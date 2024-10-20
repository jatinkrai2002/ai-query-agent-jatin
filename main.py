#main.py
#Name: Jatin K Rai
#email: jatin.rai@siu.edu
#phone: +1(618) 203 6737

import logging
from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from kubernetes import client, config
from kubernetes.config import load_config
from openai import OpenAI


KUBECONFIG_PATH = "~/.kube/config"




# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s - %(message)s',
                    filename='agent.log', filemode='a')

try:
    # Load kubeconfig
    config.load_kube_config(config_file = KUBECONFIG_PATH)
except Exception as e:
    logging.error(f"Load kube config error : {str(e)}")
    jsonify({"error": e.errors()}), 400

# Initialize Kubernetes client
v1 = client.CoreV1Api()
kube_client = client.AppsV1Api()

app = Flask(__name__)



# Pydantic model for request and response
class QueryResponse(BaseModel):
    query: str
    answer: str


apikey = "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"

#use openai object with apikey
client = OpenAI(api_key= apikey)


# Function to interact with OpenAI GPT-4
def get_gpt4_response(query: str) -> str:
    # covered into main functions.
    try:
        # Creating text completions using the updated `ChatCompletion` class
        model_name="gpt-4"

        response = client.chat.completions.create(
                model= model_name,
                messages=[{"role": "system", "content": "You are a helpful AI Agent."},
                            {"role": "user", "content": query}],
                        temperature=1,
                        max_tokens=2048,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        response_format={
                            "type": "text"
                        }
                    )
           
        text_output =  response.choices[0].message.content if  response.choices[0].message.content else "No response generated."

        logging.info(f"Generated GPT4 answer: {response.choices[0].message.content}")
        return response.choices[0].message.content
    
    except Exception as e:
       return jsonify({"error": e.errors()}), 400
    return None


# Function to handle Kubernetes queries
def handle_k8s_query(query: str) -> str:


    if "pods  in the default namespace" in query.lower():
        pods = v1.list_namespaced_pod(namespace="default")
        return f"There are {len(pods.items)} pods in the default namespace."
    # Add more query handling as needed

    elif ("pod is spawned by my-deployment" in query.lower()) or ("Which pod is spawned by my-deployment" in query.lower()):
        pods = v1.list_namespaced_pod(namespace="default")
        resp = kube_client.list_namespaced_deployment(namespace="default")
        deployment_name = "myjatinminikubeapp"
        
        for deployment in resp.items:
            deployment_name= deployment.metadata.name

        if (len(deployment_name) <= 0):
            deployment_name = "myjatinminikubeapp"
        
        spawned_pods = [pod.metadata.name[0:pod.metadata.name.find('-')] for pod in pods.items if deployment_name in pod._metadata._owner_references[0].name]
        return f"There are {spawned_pods} pod is spawned by my-deployment."

    elif ("status of the pod named" in query.lower()) or ("What is the status of the pod named" in query.lower()):
        pods = v1.list_namespaced_pod(namespace="default")
        pod_name = " "
        podstatus = ""
        for pod in pods.items:
            pod_name = pod.metadata.name
            pod = v1.read_namespaced_pod(name=pod_name, namespace="default")
            podstatus = podstatus + f" {pod_name} :  {pod.status.phase}  "

        return f"Here is the status of {podstatus}."

    elif ("nodes are there in the cluster" in query.lower()) or ("How many nodes are there in the cluster" in query.lower()):
        nodes = v1.list_node()
        return f"There are {len(nodes.items)} nodes in the default namespace."

    elif "services in the default namespace" in query.lower():
        services = v1.list_namespaced_service(namespace="default")
        return f"There are {len(services.items)} services in the default namespace."

    elif "nodes in the cluster" in query.lower():
        nodes = v1.list_node()
        return f"There are {len(nodes.items)} nodes in the cluster."

    elif "deployments in the default namespace" in query.lower():
        resp = kube_client.list_namespaced_deployment(namespace="default")
        return f"There are {len(resp.items)} deployments in the default namespace."
    
    elif "logs of pod" in query.lower():
        pods = v1.list_namespaced_pod(namespace="default")
        log = " "
        sReturnResponse =""
        for pod in pods.items:
            pod_name = pod.metadata.name
            log = v1.read_namespaced_pod_log(name=pod_name, namespace="default")
            sReturnResponse = sReturnResponse + f"Logs of pod {pod_name}: {log}"
        return sReturnResponse
    
    #Query not for AI-Agent and used for GPT4
    return "Query not recognized."



@app.route('/query', methods=['POST'])
def create_query():
    try:
        # Extract the question from the request data
        request_data = request.json
        query = request_data.get('query')
        
        # Log the question
        logging.info(f"Received query: {query}")
        
        # Here, you can implement your logic to generate an answer for the given question.
        # For simplicity, we'll just echo the question back in the answer.
        # implemented questions and answer in the format of sentence.

        """
        Q: "Which pod is spawned by my-deployment?" A: "my-pod" or (f"There are {spawned_pods} pod is spawned by my-deployment.")
        Q: "What is the status of the pod named 'example-pod'?" A: "Running" or ( Here is the status of {podstatus})
        Q: "How many nodes are there in the cluster?" A: "2" or ( f"There are {len(nodes.items)} nodes in the cluster.")
        
        """
      
        # Get the answer from Kubernetes
        answer = handle_k8s_query(query)
        # If the query is not recognized, use GPT-4
        if answer == "Query not recognized.":
            answer = get_gpt4_response(query)

            # Log the answer
        logging.info(f"Generated answer: {answer}")
    
        # Create the response model
        response = QueryResponse(query=query, answer=answer)
        return jsonify(response.dict())
    
        
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

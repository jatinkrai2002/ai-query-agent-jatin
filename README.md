## ai-query-agent-jatin

### Description: This is python based Gen AI application. The functionilty is to provide answers to the query based on kubernetes deployed application and GPT 4.0 based response.
### I have created simple python based application and deployed into the minikube envrionment with number of pods running.

### This Gen AI agent that interacts with a Kubernetes cluster to answer queries about its deployed applications on minikube environment.

**Below are pre-requisites:-**

* Use bash terminal of Visual Studio Code

* install python greater than 3 version.

* Install python library and framework such as openai fastapi kubernetes pydantic flask 

* Install  and configure Docker

* Start Docker engine

* Configure kubernetes and kubectl on docker

* Start Kubernentes under the docker eengine setting.

* Install and configure minikube 

* minikube start

* minikuber status

* kubectl config current-context

  

### Development



* eval $(minikube docker-env)

* Build simple python based application using Visual studio.

* Create simple dockerfile

* Build docker image e.g. (docker build -f dockerfile -t myjatinminikubeapp:latest .)

* Create podspec yaml file.

* Deploy podspecs to minikube container.

* kubectl apply -f .\podspec.yaml

* verify number of pods running using below commands.

* kubectl get pods

* kubectl config view

* docker images

* kubectl config get-contexts

* kubectl config current-context

* kubectl get deployments

* kubectl get svc

### Test using Postman tool.

  ![image](https://github.com/user-attachments/assets/5e0a66bd-ba72-42cc-b4e9-0b233a13737f)

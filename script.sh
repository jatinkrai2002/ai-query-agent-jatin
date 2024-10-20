Use bash terminal of VSCode
Ensure Docker install
Ensure kubernetes and kubectl
Ensure minikube install
Start Docker engine
Start Kubernentes under the docker eengine setting.
minikube start
minikuber status
kubectl config current-context
eval $(minikube docker-env)
docker build -f ../docker/Dockerfile -t clericqueryagent:latest . (docker rmi -f  clericqueryagent)
cd ../kubernetes
kubectl  apply -f deployment.yaml (or kubectl  delete -f deployment.yaml)
docker run -p 5001:5000 clericqueryagent
minikube service clericqueryagent-service --url

docker run -p 5001:5000 clericqueryagent
docker run -v ~/.kube/config:/kube/config --env KUBECONFIG=/kube/config -p 5001:5000 clericqueryagent

docker run -v ~/.kube/config:/kube/config -p 5001:5000 clericqueryagent


Q: "Which pod is spawned by my-deployment?" A: "my-pod"
Q: "What is the status of the pod named 'example-pod'?" A: "Running"
Q: "How many nodes are there in the cluster?" A: "2"

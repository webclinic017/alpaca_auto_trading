# Deployment
This directory contains all the .Dockerfiles and K8s .yaml files for deploying this app.

**Usage:**  
NOTE: Once setup, only steps 1 & 3 needs to be done.
NOTE: If only developing locally, steps 1, 4, & 5 can be skipped.
```
# SET UP
# ======
# 1) Login to Docker. This bust be done once per shell session.
docker login <registry-name>

# 2) Setup kubeconfig; cluster cert, user auth, and context. This only has to be done once.
code ~/.kube/config

# 3) Ensure you're in the correct context. Do this everytime for safety.
kubectl config get-contexts
# 3.1) If in wrong context, set the correct one.
kubectl config set current-context <context name>

# 4) By default, skaffold will not push to cloud registries. For cloud contexts, do the following. This only has to be done once.
skaffold config set --kube-context='<cloud context name>' local-cluster false

# 5) Tell skaffold which registry to push images to for your kube context. This only has to be done once.
skaffold config set --kube-context='<cloud context name>' default-repo <registry url>
```
```
# DEVELOPMENT LOOP
# ================
# dev will deploy, then watches the source code files. If skaffold sees a change it will redeploy. This is like npm run.
# It will clean up created resources once skaffold is exited (Ctrl+C)
skaffold dev

# When deving on the cloud, I suggest using run instead of dev so that docker won't push to cloud everytime the code is changed.
# --tail prints logs (stdout) to the terminal
skaffold run --tail
# When dev session is over, do
skaffold delete

# If containers are not starting, debug is useful
skaffold debug
```

**Example**
```
# LOCAL DEV
# =========
minikube start
skaffold dev
# Now you can work on your code
minikube delete
```
```
# CLOUD DEV
# =========
skaffold config set --kube-context='dss-omnisearch' local-cluster false # This only needs to be done once
docker login --username=info.loratechai.com registry-intl.cn-hongkong.aliyuncs.com
kubectl config set current-context droid-dev
skaffold run --tail
# Develop code, run 'skaffold run --tail' again to deploy changes.
skaffold delete
```

**Requirements**
- [**Docker**](https://www.docker.com/get-started): Used to build images and push to cloud container registries.
- [**Minikube**](https://minikube.sigs.k8s.io/docs/start/): Used to run a local Kubernetes cluster. It requires Kubectl to interact with it. This is only for deving.
- [**Kubectl**](https://kubernetes.io/releases/download/): Used to interact with a Kubernetes cluster. It is a standalone CLI tool.
- [**Skaffold**](https://skaffold.dev/docs/install/): Used to develop and deploy Kubernetes resources. This uses Docker and Kubectl.

## **Notes**
- Docker:

- Minikube:
    - It will automatically create a kubeconfig entry for you.
- Kubectl:
    - Edit the ~/.kube/config file to add contexts. These are useful for swapping between clusters (i.e. Minikube to cloud) or namespaces.  The cluster cert and user credentials can be found on the aliyun console under the connection information of the cluster.
    - You can have as many contexts as you like.
    - Make sure you're in the right cluster before you do anything. It is safest to start a new session everytime you work (i.e. open a fresh terminal).
    - [Here is a cheatsheet of useful commands](https://www.bluematador.com/learn/kubectl-cheatsheet)
- Skaffold:
    - Skaffold uses skaffold.yaml to know what images to build, and to which k8s deployments they belong to.
    - Edit the ~/.skaffold/config file. By default the global local-cluster variable is set to false. Do `skaffold config set --kube-context
- Kubernetes:
    - The only field that may need changing between local and cloud deployments "imagePullPolicy" ("Never" for local, "Always" for cloud)

-- If there are any other questions, ping William Gazeley on slack --

# Contents
```
deployment/
┣ container/
┃ ┗ example-image.Dockerfile
┣ example_config_files/
┃ ┣ example_kubeconfig.yaml
┃ ┗ example_skaffoldconfig.yaml
┣ kubernetes/
┃ ┣ configmaps/
┃ ┃ ┗ config_example.yaml
┃ ┣ microservices/
┃ ┃ ┗ microservice_example.yaml
┃ ┗ secrets/
┃   ┗ secrets_example.yaml
┗ README.md
```
## **container/**
Contains the .Dockerfiles.

## **example_config_files/**
Contains some exampmples of config files for CLI tools (i.e. skaffold and kubectl). These are for reference only, they do not contain valid SSH keys etc.
This folder is actually not needed.

## **kubernetes/**
Contains the kubernetes .yaml files.
### **configmaps/** ###
Contains the configmaps used by microservices. Only contains non-sensitive information.

### **microservices/** ###
Contains the .yaml files that define the microservices. Each file should (generally) contain one deployment and one service.

### **secrets/** ###
Contains the secrets used by microservices. Only contains sensitive information such as credentials.

# Conventions
- Multiword names in kubernetes use kebab-case instead of snake_case
- Every resource should be prefixed with a "---" line. This is so that if files are joined together - either manually or by CLI tools - there will be no issues.
- Declare env vars in the k8s yamls, not in dockerFiles. This was the same image can be used, but with different env vars - example usage is for swapping dev/staging/production .endpoints
- Set commands to be run by a container in the k8s yamls, not in the dockerFiles. This way the same image can be used for running different commands.
- Dockerfiles use .Dockerfile as the extension so that VSCode recognises them.

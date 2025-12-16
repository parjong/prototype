# prototype
For fast prototyping!

- https://docs.github.com/en/actions/concepts/runners/actions-runner-controller
- https://docs.github.com/en/actions/concepts/runners/support-for-arc

- https://docs.github.com/en/actions/tutorials/use-actions-runner-controller/quickstart

- https://github.com/parjong/prototype/settings/actions/runners

**STEP** Install docker

```
sudo apt install docker.io
```

**STEP** Install minikube

https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fdebian+package

**STEP** Install helm

```
sudo snap install --classic helm
```

**STEP** Start minikube cluster

```
minikube start
```

Check the status with
```
minikube kubectl -- get pods -A
```
**STEP**

```
helm install arc \
    --namespace "arc-systems" \
    --create-namespace \
    oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller

```

**STEP** Create namespace

```
minikube kubectl -- create namespace arc-runners
```

**STEP** Create secret

https://docs.github.com/en/actions/tutorials/use-actions-runner-controller/authenticate-to-the-api#authenticating-arc-with-a-personal-access-token-classic
```
minikube kubectl -- create secret generic pre-defined-secret \
    --namespace=arc-runners \
    --from-literal=github_token=$GITHUB_PAT
```

**STEP**
```
helm install "self-hosted-k8n" \
    --namespace "arc-runners" \
    --set githubConfigUrl="https://github.com/parjong/prototype" \
    --set githubConfigSecret.github_token="${GITHUB_PAT}" \
    oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set
```
https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml

<!-- helm uninstall self-hosted-k8n --namespace arc-runners -->

```
helm list -A
```

```
minikube kubectl -- get pods --namespace arc-runners
```

**Alternative**




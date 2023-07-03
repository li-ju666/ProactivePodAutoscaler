## Proactive Autoscaling for Edge Computing Systems with Kubernetes

This repository contains the code and experiments for the paper:
> [Proactive Autoscaling for Edge Computing Systems with Kubernetes](https://dl.acm.org/doi/pdf/10.1145/3492323.3495588)
> 
> [UCC '21](https://dl.acm.org/conference/ucc)

---
### Structure of the codes
The codes contain 3 parts: 
1. Scripts for the deployment of the workspace
2. Scripts for the deployment of the example application in the paper
3. Impelementation of the proposed Proactive Pod Autoscaler (PPA)

---
Note: 
The deployment of the application and the PPA on Kubernetes replies on the images on Dockerhub. 
You are expected to build the worker and PPA containers locally and push them to your own Dockerhub. 
kind create cluster --config cluster.yaml
kubectl create namespace prometheus
helm install prom -n prometheus prometheus-community/kube-prometheus-stack \
    --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false \
    --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
    --set prometheus.prometheusSpec.evaluationInterval=5s \
    --set prometheus.prometheusSpec.scrapeInterval=5s
helm install adapter -n prometheus prometheus-community/prometheus-adapter \
    --set prometheus.url=http://prom-kube-prometheus-stack-prometheus 
VERSION=v1.1.0
kubectl apply -f https://github.com/jthomperoo/custom-pod-autoscaler-operator/releases/download/${VERSION}/cluster.yaml

envsubst < /config.tmp > /config.yaml
wget -O /model_dir/model ${ModelLink}
wget -O /model_dir/scaler ${ScalerLink}
python3 /updateModel.py & /app/custom-pod-autoscaler
# /app/custom-pod-autoscaler

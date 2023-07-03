import json, sys, joblib, numpy
from tensorflow import keras
from math import ceil
import os
from helpers import get_helper
from pandas import read_csv
from statsmodels.tsa.arima.model import ARIMA

if 'Threshold' in os.environ:
    expected = float(os.environ['Threshold'])
else: 
    expected = 0.8

def main():
    # Parse JSON into a dict
    spec = json.loads(sys.stdin.read())
    evaluate(spec)

def static_policies(metrics, limits, replicas):
    result = ceil(metrics[0]/expected/(limits[0]/replicas))
    # result = round(metrics[4]/5000)
    return result


def evaluate(spec):
    # TODO: evaluate maximum replicas
    max_replicas = 8

    metrics_values = json.loads(spec["metrics"][0]["value"])
    numOfTargets = 7
    # TODO: check if all metrics are here
    if len(metrics_values) == numOfTargets:
        current_metrics = []
        metrics_names = ['cpu_usage', 'memory_working_set_bytes', 'network_receive_bytes',
                         'network_transmit_bytes', 'requests_rate']
        for metric in metrics_names:
            current_metrics.append(metrics_values[metric])
        cpu_requests = metrics_values['kube_pod_container_resource_requests_cpu_cores']
        mem_requests = metrics_values['kube_pod_container_resource_requests_memory_bytes']
        with open('/idel.log', 'a+') as f:
            f.write(str(cpu_requests - current_metrics[0]) + ',' + \
                    str(cpu_requests) + '\n')
        try:
            helper = get_helper(os.environ['ModelType'])
            model = helper.load_model('/model_dir/model') 
            # model = keras.models.load_model("/model_files/model")
            scaler = joblib.load("/model_dir/scaler")
            test_x = numpy.array(current_metrics).reshape(1, 5)
            test_x = scaler.transform(test_x).reshape(1, 1, 5)
            prediction = helper.predict(model, test_x)
            result = scaler.inverse_transform(prediction)[0].tolist()
            with open('/realtime.log', 'a+') as f:
                forcasted = str(result[0]) + '\n'
                f.write(forcasted)
                f.write(str(current_metrics[0]) + ',')
        except Exception as e:
            with open('/error.log', 'a+') as f:
                f.write(str(e)+'\n')
            result = current_metrics
        # target_replicas = static_policies(current_metrics, (cpu_requests, mem_requests), 
        #         spec['resource']['status']['replicas'])
        target_replicas = static_policies(result, (cpu_requests, mem_requests), 
                spec['resource']['status']['replicas'])
    else:
        target_replicas = spec['resource']['status']['replicas']

    # Build JSON dict with targetReplicas
    with open('/performance.log', 'a+') as f:
        information = str(metrics_values['cpu_usage']) + ',' +\
            str(metrics_values['requests_rate']) + ',' +\
            str(spec['resource']['status']['replicas']) + '\n'
        f.write(information)
    if target_replicas <= max_replicas:
        evaluation = {"targetReplicas": target_replicas}
    else: 
        evaluation = {"targetReplicas": max_replicas}

    # Output JSON to stdout
    sys.stdout.write(json.dumps(evaluation))


if __name__ == "__main__":
    main()

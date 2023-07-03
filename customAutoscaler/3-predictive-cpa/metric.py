import json
import sys
import os

expected = 0.8

def main():
    # Parse spec into a dict
    spec = json.loads(sys.stdin.read())['kubernetesMetrics']
    extract(spec)

def extract(spec):
    # Metrics: 
    # 1. cpu usage; 2. cpu requests
    # 3. mem usage; 4. mem requests
    # 5. network transmitted; 6. network received
    # 7. custom metrics (tasks received)
    numOfTargets = 7
    # format spec data into pipe-out dictionary
    pipe_out = dict()
    for metric in spec:
        num_replicas = metric['current_replicas']
        if metric['spec']['type'] == 'Pods':
            name = metric['spec']['pods']['metric']['name']
            value = 0
            for _, pod_info in metric['pods']['pod_metrics_info'].items():
                value += pod_info['Value']
        else:
            # custom metric: calculate rate of requests
            name = 'requests_rate'
            value = metric['object']['current']['value']
            try: 
                with open('/last_tasks.log', 'r') as f: 
                    last = int(f.read())
            except: 
                last = 0
            with open('/last_tasks.log', 'w') as f: 
                f.write(str(value))
            value -= last
        pipe_out[name] = value

    # if all metrics are collected, store data
    if len(pipe_out) == numOfTargets:
        toBeStored = [
                pipe_out['cpu_usage'], 
                pipe_out['memory_working_set_bytes'], 
                pipe_out['network_receive_bytes'], 
                pipe_out['network_transmit_bytes'], 
                pipe_out['requests_rate']]
        toBeStored = ','.join(list(map(str, toBeStored)))
        with open("/metrics_log.csv", "a+") as fp:
            fp.write(toBeStored+"\n")
    # Generate some JSON to pass to the evaluator
    sys.stdout.write(json.dumps(pipe_out))

if __name__ == "__main__":
    main()


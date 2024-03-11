import subprocess
import re
import statistics
from multiprocessing import Process
from datetime import datetime

ip_addresses = ["hepsiburada.com", "abv.bg", "skroutz.gr", "sinoptik.ua", "spiegel.de", "mail.ru", "flipkart.com", "redmart.lazada.sg", "baidu.com", "mixi.jp"]

def run_tracert(ip_address, num_runs):
    results = []
    for _ in range(num_runs):
        tracert_process = subprocess.Popen(["tracert", ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        tracert_output, _ = tracert_process.communicate()
        results.append(tracert_output)

    latencies = parse_tracert_results(results)

    if latencies:
        min_latency = min(latencies)
        max_latency = max(latencies)
        avg_latency = statistics.mean(latencies)

        time_date = datetime.now()
        time_date_str = time_date.strftime("%d-%m-%Y_%H-%M")
        with open(f"{time_date_str}.txt", "a") as output_file:
            output_file.write(f"{ip_address} traceroute count {num_runs} min:{min_latency}, max:{max_latency}, avg:{avg_latency:.2f}\n")

def parse_tracert_results(results):
    ping_values = []
    for result in results:
        latencies = []
        lines = result.splitlines()
        for line in lines:
            latencies_line = re.findall(r'\d+ ms', line)
            if latencies_line:
                latencies.extend([int(latency.split()[0]) for latency in latencies_line])
        ping_values.extend(latencies[-3:])
    return ping_values

if __name__ == "__main__":
    processes = []
    for ip_address in ip_addresses:
        for i in range(10):
            process = Process(target=run_tracert, args=(ip_address, (i+1) * 10))
            processes.append(process)
            process.start()
    for process in processes:
        process.join()

    print("All tracert processes completed.")
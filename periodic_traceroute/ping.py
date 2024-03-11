import subprocess
from datetime import datetime
import re
from collections import defaultdict
from multiprocessing import Pool


def ping_website(website, num_runs):
    command = f"ping -n {num_runs} {website}"
    output = subprocess.run(command, shell=True, capture_output=True)
    output_text = output.stdout.decode()
    time_values = re.findall(r"time=(\d+)ms", output_text)
    return website, num_runs, time_values

if __name__ == "__main__":
    time_date = datetime.now()
    time_date_str = time_date.strftime("%d-%m-%Y_%H-%M")
    path = f"{time_date_str}.txt"
    ip_addresses = ["hepsiburada.com", "abv.bg", "skroutz.gr", "sinoptik.ua", "spiegel.de", "mail.ru", "flipkart.com", "redmart.lazada.sg", "baidu.com", "mixi.jp"]

    with open(path, "a") as file:
        with Pool() as pool:
            results = []
            for address in ip_addresses:
                for i in range(10):
                    num_runs = (i + 1) * 10
                    results.append(pool.apply_async(ping_website, (address, num_runs)))

            times_dict = defaultdict(list)

            for result in results:
                address, ping_count, time_values = result.get()
                if time_values:
                    time_values = [int(value) for value in time_values]
                    times_dict[(address, ping_count)].extend(time_values)
            for (address, ping_count), time_values in times_dict.items():
                if time_values:
                    minimum = min(time_values)
                    maximum = max(time_values)
                    average = sum(time_values) / len(time_values)
                    file.write(f"{address} traceroute count {ping_count} min:{minimum}, max:{maximum}, avg:{average:.2f}\n")
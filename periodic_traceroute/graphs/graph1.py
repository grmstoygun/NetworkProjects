import os
import matplotlib.pyplot as plt

min_values = {}
max_values = {}
avg_values = {}

data_file_path = "ping_data\\27-10-2023_09-02.txt"
with open(data_file_path, 'r') as file:
    lines = file.readlines()

for line in lines:
    parts = line.split()
    website = parts[0]
    min_ping, max_ping, avg_ping = None, None, None

    for part in parts:
        if "min:" in part:
            min_ping = float(part.split(':')[1].replace(',', ''))
        elif "max:" in part:
            max_ping = float(part.split(':')[1].replace(',', ''))
        elif "avg:" in part:
            avg_ping = float(part.split(':')[1].replace(',', ''))

    if min_ping is not None and max_ping is not None and avg_ping is not None:
        if website not in min_values:
            min_values[website] = []
        if website not in max_values:
            max_values[website] = []
        if website not in avg_values:
            avg_values[website] = []

        min_values[website].append(min_ping)
        max_values[website].append(max_ping)
        avg_values[website].append(avg_ping)

overall_min = {website: min(min_values[website]) for website in min_values}
overall_max = {website: max(max_values[website]) for website in max_values}
overall_avg = {website: sum(avg_values[website]) / len(avg_values[website]) for website in avg_values}

websites = overall_min.keys()
min_ping_values = [overall_min[website] for website in websites]
max_ping_values = [overall_max[website] for website in websites]
avg_ping_values = [overall_avg[website] for website in websites]

plt.figure(figsize=(12, 6))
plt.bar(websites, min_ping_values, label='Min Latency', color='b', alpha=0.7)
plt.bar(websites, max_ping_values, label='Max Latency', color='r', alpha=0.7)
plt.bar(websites, avg_ping_values, label='Avg Latency', color='g', alpha=0.7)
plt.xlabel('Websites')
plt.ylabel('Latency Values(ms)')
plt.title('Latency Values On The Same Date and Time On Different Geographical Distances')
plt.legend()
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
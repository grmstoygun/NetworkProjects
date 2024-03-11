import re
import matplotlib.pyplot as plt

min_values = []
max_values = []
avg_values = []
time_labels = ["09:02:48", "13:02:03", "21:14:34"]

website = "mail.ru"

with open("graph2_data1.txt", "r") as file:
    lines = file.readlines()

min_pattern = re.compile(r'min:(\d+)')
max_pattern = re.compile(r'max:(\d+)')
avg_pattern = re.compile(r'avg:([\d.]+)')

for i in range(0, len(lines), 10):
    time_period_data = lines[i:i + 10]

    min_val = float("inf")
    max_val = float("-inf")
    sum_val = 0

    for line in time_period_data:
        min_match = min_pattern.search(line)
        max_match = max_pattern.search(line)
        avg_match = avg_pattern.search(line)

        if min_match and max_match and avg_match:
            min_val = min(min_val, int(min_match.group(1)))
            max_val = max(max_val, int(max_match.group(1)))
            sum_val += float(avg_match.group(1))
    avg_val = sum_val / len(time_period_data)

    min_values.append(min_val)
    max_values.append(max_val)
    avg_values.append(avg_val)
    ##time_labels.append(f"Time {i // 10 + 1}")

overall_min = min(min_values)
overall_max = max(max_values)
overall_avg = sum(avg_values) / len(avg_values)

plt.figure(figsize=(10, 6))
plt.plot(time_labels, min_values, label="Minimum")
plt.plot(time_labels, max_values, label="Maximum")
plt.plot(time_labels, avg_values, label="Average")
plt.xlabel("Time of the Day")
plt.ylabel("Ping Values")
plt.title(f"{website} Latency on The Day Time At Different Times")
plt.legend()
plt.grid(True)
plt.show()
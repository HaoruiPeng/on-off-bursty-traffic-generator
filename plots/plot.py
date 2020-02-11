import os
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt


time = np.array([])
nodes = [str(n) for n in range(100)]
Dict = dict((key, np.array([])) for key in nodes)
with open("trace.csv", "r") as file:
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
        if row["Mode"] == "None":
            time = np.append(time, float(row["Arrival"]))
            Dict[row["Node"]] = np.append(Dict[row["Node"]], float(row["Arrival"]))


arrivals = 0
index = 0
end = time[-1]

inter_arrivals = np.array([])
time_stamps = np.array([])

fig_all, axs_all = plt.subplots(3,1,figsize=(12,12))
for t in np.arange(0.5, end+0.5, 0.5):
    while index < len(time) and time[index] <= t:
        arrivals += 1
        index += 1
    inter_arrivals = np.append(inter_arrivals, arrivals)
    time_stamps = np.append(time_stamps, t)
    arrivals = 0
    if index >= len(time):
        break

axs_all[0].plot(time_stamps, inter_arrivals)

arrivals = 0
index = 0
inter_arrivals = np.array([])
time_stamps = np.array([])

for t in np.arange(1, end+1, 1):
    while index < len(time) and time[index] <= t:
        arrivals += 1
        index += 1
    inter_arrivals = np.append(inter_arrivals, arrivals)
    time_stamps = np.append(time_stamps, t)
    arrivals = 0
    if index >= len(time):
        break
axs_all[1].plot(time_stamps, inter_arrivals)

arrivals = 0
index = 0
inter_arrivals = np.array([])
time_stamps = np.array([])

for t in np.arange(25, end, 25):
    while index < len(time) and time[index] <= t:
        arrivals += 1
        index += 1
    inter_arrivals = np.append(inter_arrivals, arrivals)
    time_stamps = np.append(time_stamps, t)
    arrivals = 0
    if index >= len(time):
        break
axs_all[2].plot(time_stamps, inter_arrivals)

observes = [str(n) for n in [2, 4,1]]
counter = 0
figs, axs = plt.subplots(len(observes),1,figsize=(12,12))
for key in observes:
    time = Dict[key]
    arrivals = 0
    index = 0
    end = time[-1]

    inter_arrivals = np.array([])
    time_stamps = np.array([])

    for t in np.arange(1, end+1, 1):
        while index < len(time) and time[index] <= t:
            arrivals += 1
            index += 1
        inter_arrivals = np.append(inter_arrivals, arrivals)
        time_stamps = np.append(time_stamps, t)
        arrivals = 0
        if index >= len(time):
            break

    axs[counter].plot(time_stamps, inter_arrivals)
    counter += 1

plt.show()

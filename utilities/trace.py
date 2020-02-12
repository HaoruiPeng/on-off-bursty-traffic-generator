import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

class Trace:

    def __init__(self, trace_file_path, log=False):
        self.log = log
        if log is True:
            self.__trace_file = open(trace_file_path, 'w+')
            self.__trace_file.write('Event,Node,Arrival,Mode\n')
        else:
            self.__trace_file = None
        self.keys = ['event_type', 'node_id', 'arrival_time', 'mode']
        self.Dict = dict((key, []) for key in self.keys)
        self.plot_path = None
        self.urllc = {}

        self.queue_length = np.empty((0,2), int)
        self.waste_trace = np.empty((0,2), int)
        self.loss_trace = np.empty((0,2), int)
        self.decision_trace = np.empty((0,2), int)


    def close(self):
        if self.log is True:
            self.__trace_file.close()
        else:
            pass

    def write_trace(self, entry):
        if self.log is True:
            self.__trace_file.write(str(entry[self.keys[0]]) + ',' + str(entry[self.keys[1]]) + ','
                                    + str(entry[self.keys[2]]) + ',' + str(entry[self.keys[3]]) + '\n')

        for i in range(len(entry)):
            k = self.keys[i]
            self.Dict[k] = np.append(self.Dict[k], entry[k])

    def plot_arrivals(self):
        time = np.array([])
        for i in range(len(self.Dict["arrival_time"])):
            if self.Dict["mode"][i] is None:
                time = np.append(time, self.Dict["arrival_time"][i])

        end = time[-1]
        print("simulation length: {}".format(end))
        print("total arrival: {}".format(len(time)))
        arrival_per_ms = len(time)/end
        print(arrival_per_ms)
        arrivals = 0
        index = 0

        inter_arrivals = np.array([])
        time_stamps = np.array([])

        fig_1, axs_1 = plt.subplots(3,1,figsize=(12,12))
        fig_2, axs_2 = plt.subplots(3,1,figsize=(12,12))

        for t in np.arange(0.5, end+0.5, 0.5):
            while index < len(time) and time[index] <= t:
                arrivals += 1
                index += 1
            inter_arrivals = np.append(inter_arrivals, arrivals)
            time_stamps = np.append(time_stamps, t)
            arrivals = 0
            if index >= len(time):
                break

        axs_1[0].plot(time_stamps, inter_arrivals)
        axs_1[0].axhline(arrival_per_ms*0.5, c="C3")
        axs_2[0].plot(time_stamps, inter_arrivals/12)
        axs_2[0].axhline(arrival_per_ms/24, c="C3")


        arrivals = 0
        index = 0
        inter_arrivals = np.array([])
        time_stamps = np.array([])

        for t in np.arange(10, end+5, 10):
            while index < len(time) and time[index] <= t:
                arrivals += 1
                index += 1
            inter_arrivals = np.append(inter_arrivals, arrivals)
            time_stamps = np.append(time_stamps, t)
            arrivals = 0
            if index >= len(time):
                break

        axs_1[1].plot(time_stamps, inter_arrivals)
        axs_1[1].axhline(arrival_per_ms*10, c="C3")
        axs_2[1].plot(time_stamps, inter_arrivals/(24*10))
        axs_2[1].axhline(arrival_per_ms/24, c="C3")


        arrivals = 0
        index = 0
        inter_arrivals = np.array([])
        time_stamps = np.array([])

        for t in np.arange(100, end+10, 100):
            while index < len(time) and time[index] <= t:
                arrivals += 1
                index += 1
            inter_arrivals = np.append(inter_arrivals, arrivals)
            time_stamps = np.append(time_stamps, t)
            arrivals = 0
            if index >= len(time):
                break

        axs_1[2].plot(time_stamps, inter_arrivals)
        axs_1[2].axhline(arrival_per_ms*100,c="C3")
        axs_2[2].plot(time_stamps, inter_arrivals/(24*100))
        axs_2[2].axhline(arrival_per_ms/24,c="C3")

    def show_plot(self):
        plt.show()

import sys
import os
from events.event_heap import EventHeap
import numpy as np
import time
import csv
from nodes.file_node import FileNode
from nodes.periodic_node import PeriodicNode


class Simulation:
    """
    Simulation for a network slicing strategy on MAC layer of a massive MIMO network

    Attributes
    ----------


    Methods
    -------
    run()
        Runs the simulation the full simulation length
    """

    _PERIODIC = 0
    _FILE = 1
    _SPORADIC = 2

    _MODE_SWITCH = 0
    _PACKET_ARRIVAL = 1

    _ON = 1
    _OFF = 0

    def __init__(self, config, no_file, no_periodic, inner_periods, inner_variance, t_on, t_off, trace, seed=None):
        """
        Initialize simulation object

        Parameters
        ----------
        no_periodic:
        no_file:
        inner_periods:

        """

        self.trace = trace
        self.time = 0.0
        self.seed = seed

        self.simulation_length = config.get('simulation_length')
        self.frame_length = config.get('frame_length')

        self.event_heap = EventHeap()
        periods = np.random.randint(1, 10, size=no_periodic)
        sum = 0
        for p in periods:
            sum += 1/p*0.5
        print(sum)
        # TODO: Here the traffic is canceled from taking new variables
        self.Nodes = [FileNode(inner_periods, inner_variance, t_on, t_off) for i in range(no_file)] + [PeriodicNode(p, inner_variance) for p in periods]
        #Decision : A dict with all the decisicion that the actuator look up every coherence interval
        #TODO:The initial number of users should follow the traffic distributtion of each slice
        node_index = 0
        for n in self.Nodes:
            # Initialize nodes and their arrival times
            self.__initialize_nodes(n, node_index)
            node_index += 1


    def __initialize_nodes(self, _node, _index):
        type = _node.get_type()
        if type == self._FILE:
            next_switch, next_mode = _node.mode_switch.get_init()
            self.event_heap.push(self._MODE_SWITCH,
                                 self.time + next_switch,
                                 _index, next_mode)
        if type == self._PERIODIC:
            next_arrival = _node.packet_generator.get_init()
            self.event_heap.push(self._PACKET_ARRIVAL,
                                 self.time + next_arrival,
                                 _index)
#################################################################################################################
## Evnets Handling
#################################################################################################################

    def __handle_event(self, event):
        # Event switcher to determine correct action for an event
        event_actions = {
            self._MODE_SWITCH: self._handle_mode_switch,
            self._PACKET_ARRIVAL: self.__handle_packet_arrival,

        }
        event_actions[event.type](event)


    def __handle_packet_arrival(self, event):
        assert(event.mode == None)
        node_index = event.get_node()
        node = self.Nodes[node_index]
        # if node.mode == self._ON:
        #     print("[{}] packet arrival for node {}, node mode {} On".format(self.time, node_index, node_index))
        # elif node.mode == self._OFF:
        #     print("[{}] packet arrival for node {}, node {} mode OFF".format(self.time, node_index, node_index))
        # else:
        #     print("[{}] wrong node mode {}".format(self.time, node.mode))

        if node.node_type == self._FILE and node.mode == self._OFF:
            pass
        else:
            entry = event.get_entry()
            self.trace.write_trace(entry)
            print("write entry")
            next_arrival = node.packet_generator.get_next()
            self.event_heap.push(event.type,
                             self.time + next_arrival,
                             event.get_node())
        del event
#################################################################################################################
## Methods
#################################################################################################################

    def _handle_mode_switch(self, event):
        node = self.Nodes[event.get_node()]
        assert(node.node_type == self._FILE)
        node.mode = event.mode
        next_switch, next_mode = node.mode_switch.get_next(event.mode)
        entry = event.get_entry()
        self.trace.write_trace(entry)
        self.event_heap.push(self._MODE_SWITCH,
                             self.time + next_switch,
                             event.get_node(), next_mode)
        if node.mode == self._ON:
            print("[{}] Node.{} ON".format(self.time, event.get_node()))
            self.event_heap.push(self._PACKET_ARRIVAL,
                                 self.time,
                                 event.get_node())
        else:
            print("[{}] Node.{} OFF".format(self.time, event.get_node()))

        del event
#################################################################################################################
## Simulation Run
#################################################################################################################

    def run(self):
        """ Runs the simulation """
        current_progress = 0
        print("\n[Time {}] Simulation start.".format(self.time))
#        print("Size: {}".format(self.event_heap.get_size()))
        # for k in self.event_heap.get_heap():
        #     print(k)
        while self.time <= self.simulation_length:
#            print("[Time {}] Event heap size {}".format(self.time, self.event_heap.size()))
            next_event = self.event_heap.pop()[3]
            # print("Handle event: {} generated at time {}".format(next_event.type, next_event.time))

            # Advance time before handling event
            self.time = next_event.time
            progress = np.round(100 * self.time / self.simulation_length)

            if progress > current_progress:
                current_progress = progress
            self.__handle_event(next_event)

        print('\n[Time {}] Simulation complete.'.format(self.time))

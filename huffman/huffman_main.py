# -*- coding: utf-8 -*-
"""
Massive MIMO factory simulation

This library provides a network simulator for a factory floor with a number of machines with control traffic and a
number of alarm nodes with alarm traffic. The library is built to be highly configurable.
"""

import json
import time
import numpy as np

from utilities.stats import Stats
from huffman.huffman_simulation import HuffmanSimulation as Simulation
from huffman.huffman_tree import HuffmanTree
from huffman.huffman_node import HuffmanNode

__author__ = "Amalia Paulsson"

class HuffmanMain():
    def run(stats):
        # Load simulation parameters
        with open('../default_config.json') as config_file:
            config = json.load(config_file)

        # Only use multi run
        if config.get("multi_run"):
            stopping_criteria = 1
            iteration = 1

            while stats.stats.get('no_alarm_arrivals') < 1000:
                stats.clear_stats()

                # Generate random alarm probabilities. Every simulation has its own base_seed, set to current time.
                # For every configuration and generated event the seed is increased by 1.
                seed = int(time.time())
                np.random.seed(seed)
                seed += 1
                alarm_node_probabilities = np.random.rand(config.get('no_alarm_nodes'), 1) * 0.5

                # Change to per frame probabilities
                alarm_node_probabilities = alarm_node_probabilities / (
                        config.get('simulation_length') * 1000 / config.get('frame_length'))

                # Generate pilot sequences based on huffman tree
                huffman_tree = HuffmanTree(alarm_node_probabilities)
                alarm_node_pilot_sequences = huffman_tree.pilot_sequences

                huffman_alarm_arrivals = []

                # Create Huffman nodes
                for i in range(len(alarm_node_probabilities)):
                    huffman_alarm_arrivals.append(
                        HuffmanNode(i, alarm_node_probabilities[i], alarm_node_pilot_sequences[i]))

                custom_control_arrivals = None

                if config['custom_control_arrivals']:
                    custom_control_arrivals = []
                    # Just replicating what's in the config file
                    for i in range(config.get('no_control_nodes')):
                        entry = {'distribution': 'uniform', 'settings': {'mean_arrival_time': 50}, 'max_attempts': 10}
                        custom_control_arrivals.append(entry)

                # Update the run configuration number, should start with zero
                stats.stats['config_no'] = iteration - 1

                #Update the base_seed
                stats.stats['base_seed'] = seed

                # Set new config parameters here by overriding the config file
                # e.g. config['max_attempts'] =R 2*(i+1)
                config['no_alarm_nodes'] = iteration * 500

                print('{} alarm nodes'.format(config.get('no_alarm_nodes')))

                # Run the simulation with new parameters
                simulation = Simulation(config, stats, huffman_alarm_arrivals, custom_control_arrivals, seed=seed)
                simulation.run()

                print('Seed: {}'.format(simulation.base_seed))

                # Process, save and print the results
                stats.process_results()
                stats.save_stats()
                stats.print_stats()
                iteration += 1


        # Close files
        stats.close()

    #def get_arrival_collisions_misscon():

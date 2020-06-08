# -*- coding: utf-8 -*-
"""
Massive MIMO factory simulation

This library provides a network simulator for a factory floor with a number of machines with control traffic and a
number of alarm nodes with alarm traffic. The library is built to be highly configurable.
"""

import json
"""
Massive MIMO factory simulation
This library provides a network simulator for a factory floor with a number of machines with control traffic and a
number of alarm nodes with alarm traffic. The library is built to be highly configurable.
"""

import json
import time
import numpy as np

from utilities.stats import Stats
from binary.binary_simulation import BinarySimulation as Simulation

__author__ = "Jon Stålhammar, Christian Lejdström, Emma Fitzgerald"

class BinaryMain():
    def run(stats):
        # Load simulation parameters
        with open('../default_config.json') as config_file:
            config = json.load(config_file)

        custom_alarm_arrivals = None
        custom_control_arrivals = None

        # Declare custom arrival distributions
        # Length of the array need to match the number of nodes
        # Format of each should be dictionary with following keys, e.g.:
        # Note, below blocks can also be added in the multi_run loop
        # {
        #   'distribution': 'exponential',
        #   'settings': { 'mean_arrival_time': 1000 }
        #   'max_attempts': 10
        # }

        if config['custom_alarm_arrivals']:
            custom_alarm_arrivals = []

            # Just replicated what's in the config file
            for i in range(config.get('no_alarm_nodes')):
                entry = {'distribution': 'exponential', 'settings': {'mean_arrival_time': 1000}, 'max_attempts': 10}
                custom_alarm_arrivals.append(entry)

        if config['custom_control_arrivals']:
            custom_control_arrivals = []

            # Just replicating what's in the config file
            for i in range(config.get('no_control_nodes')):
                entry = {'distribution': 'exponential', 'settings': {'mean_arrival_time': 50}, 'max_attempts': 10}
                custom_control_arrivals.append(entry)

        # Override the default config and run multiple simulations
        if config.get("multi_run"):
            stopping_criteria = 1
            i = 1

            while stats.stats.get('no_alarm_arrivals') < 1000:
                stats.clear_stats()

                # Generate random seed. Every simulation has its own base_seed, set to current time.
                # For every configuration and generated event the seed is increased by 1.
                seed = int(time.time())
                np.random.seed(seed)
                seed += 1

                # Update the run configuration number, should start with zero
                stats.stats['config_no'] = i - 1

                # Set new config parameters here by overriding the config file
                # e.g. config['max_attempts'] =R 2*(i+1)
                config['no_alarm_nodes'] = i * 500

                print('{} alarm nodes'.format(config.get('no_alarm_nodes')))

                # Run the simulation with new parameters
                simulation = Simulation(config, stats, custom_alarm_arrivals, custom_control_arrivals, seed)
                simulation.run()

                print('Seed: {}'.format(simulation.base_seed))

                #Update the base_seed in stats
                stats.stats['base_seed'] = simulation.base_seed

                # Process, save and print the results
                stats.process_results()
                stats.save_stats()
                stats.print_stats()
                i += 1
        else:
            # Run a single simulation with default parameters
            simulation = Simulation(config, stats, custom_alarm_arrivals, custom_control_arrivals)
            simulation.run()
            stats.process_results()
            stats.save_stats()
            stats.print_stats()

        # Close files
        stats.close()

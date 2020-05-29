import json
import time
import numpy as np

from utilities.stats import Stats
from huffman.huffman_simulation import HuffmanSimulation as Simulation
from huffman.huffman_tree import HuffmanTree
from huffman.huffman_node import HuffmanNode
from huffman.huffman_main import HuffmanMain as Main

__author__ = "Amalia Paulsson"

if __name__ == '__main__':

    with open('../default_config.json') as config_file:
        config = json.load(config_file)

    time_string = time.strftime('%Y%m%d_%H%M%S')
    simulation_name = config.get('simulation_name')
    i = 1
    results = []

    for i in range(10):
        log_file_path = '../logs/' + time_string + '_' + simulation_name + str(i) + '_queue_log.csv'
        stats_file_path = '../stats/' + time_string + '_' + simulation_name + str(i) + '_stats.csv'

        # Initialize stats and logger
        stats = Stats(stats_file_path, log_file_path)

        print('Simulation nbr: ', i)
        results.append(Main.run(stats))


    #Create file to store results
    #stat_tot = Stats('../stats/huffman_10_sim.csv','../logs/huffman_10_sim.csv')
    #tot_stats_file = open('../stats/huffman_10_sim.csv', 'w')

    #Write mean and confidence interval for no_alarm_arrivals, no_collisions & no_missed_controls
    #for sim in results:
    #    for conf in sim:
    #        stats.__calc_confidence_interval(conf['no_alarm_arrivals'])
    #        tot_stats_file.write(results)

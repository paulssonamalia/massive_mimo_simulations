import json
import time

from utilities.stats import Stats
from binary.binary_simulation import BinarySimulation as Simulation
from binary.binary_main import BinaryMain as Main

__author__ = "Jon Stålhammar, Christian Lejdström, Emma Fitzgerald"

if __name__ == '__main__':
    with open('../binary/default_config.json') as config_file:
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

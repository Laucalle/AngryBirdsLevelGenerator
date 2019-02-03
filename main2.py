import datetime
import time
import os
import json
import sys
import AngryBirdsGA.XmlHelpers as xml
import AngryBirdsGA.evolution as ea

def cleanDirectory(path):
    for f in os.listdir(path):
        os.remove(os.path.join(path,f))

def main():
    timestamp = datetime.datetime.today()
    init = time.time()

    project_root = os.getcwd()
    config_file = open(os.path.join(project_root, sys.argv[1]), 'r')
    config_param = json.load(config_file)
    population_size = config_param['population_size']
    number_of_generations = config_param['number_of_generations']
    number_of_parents = config_param['percent_of_parents']
    number_of_mutations = [[config_param['percent_of_mutations_type']],
                           [config_param['percent_of_mutations_rotation']],
                           [config_param['percent_of_mutations_x']],
                           [config_param['percent_of_mutations_y']],
                           [config_param['percent_of_mutations_mat']]]
    ea.MAX_B = config_param['max_blocks']
    ea.MIN_B = config_param['min_blocks']

    game_path = os.path.join(os.path.dirname(project_root), config_param['game_path'])
    write_path = os.path.join(os.path.dirname(project_root),config_param['write_path'])
    read_path = os.path.join(os.path.dirname(project_root),config_param['read_path'])
    log_path = os.path.join(project_root, config_param['log_dir'])
    log_base_name = config_param['log_base_name']


    evolution = ea.Evolution(game_path=game_path, write_path=write_path,read_path=read_path)

    worst_evaluated = 0
    worst_evaluated = evolution.initEvolution(population_size= population_size,
                                            initialization_method=ea.LevelIndividual.initPreMadeDiscrete,
                                            fitness_params=[worst_evaluated])

    cleanDirectory(write_path)
    cleanDirectory(read_path)
    log_object = {}
    fill = len(str(number_of_generations))
    same_generation_strike = 0
    last_generation_worst = None
    for generation in range(number_of_generations):
        population, max_evaluated = evolution.runGeneration(fitness_params=[worst_evaluated],
                                                            mutation_params=number_of_mutations,
                                                            selection_params=[number_of_parents],
                                                            replacement_params=[population_size])
        cleanDirectory(write_path)
        cleanDirectory(read_path)
        log_object[str(generation).zfill(fill)] = {
            "entropy" : ea.informationEntropy(population, 4),
            "best" : population[0].fitness,
            "avg" : (sum(map(lambda x: x.fitness, population)) / len(population)),
            "worst" : max(population, key=lambda x: x.fitness).fitness
        }
        print(log_object[str(generation).zfill(fill)])
        #print("best --> base " + str(population[0].base_fitness) + " overlapping " + str(population[0].n_overlapping) + " fit " + str(population[0].fitness) + "\n")
        if max(population, key=lambda x: x.fitness).fitness == last_generation_worst:
            same_generation_strike+=1
        else:
            same_generation_strike = 0
        if same_generation_strike>10 or population[0].fitness < 0.01:
            break

        last_generation_worst = max(population, key=lambda x: x.fitness).fitness
        #xml.writeXML(population[0], os.path.join(project_root, log_path + "/level-0-"+ log_base_name  +
        #                                             timestamp.strftime("%y%m%d_%H%M%S") + ".xml"))
    end = time.time()
    final_log = {'config': config_param,
                 'execution_time': (end - init),
                 'execution':log_object}
    f = open(os.path.join(project_root, log_path + "/" + log_base_name + timestamp.strftime("_%y%m%d_%H%M%S") + ".json"), 'w')
    json.dump(final_log, f , indent=2)
    xml.writeXML(population[0], os.path.join(project_root, log_path + "/level-0-" + log_base_name +
                                             timestamp.strftime("%y%m%d_%H%M%S") + ".xml"))

if __name__ == "__main__":
    main()
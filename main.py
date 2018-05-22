import datetime
import time
import os
import json
import sys
import AngryBirdsGA.XMLHelpers as xml
import AngryBirdsGA.evolution as ea

def cleanDirectory(path):
    for f in os.listdir(path):
        os.remove(os.path.join(path,f))

def main():
    timestamp = datetime.datetime.today()
    init = time.time()
    ea.Random = ea.random_set_seed(1526992711.6456888)
    project_root = os.getcwd()
    config_file = open(os.path.join(project_root, sys.argv[1]), 'r')
    config_param = json.load(config_file)
    population_size = config_param['population_size']
    number_of_generations = config_param['number_of_generations']
    number_of_parents = config_param['percent_of_parents']
    number_of_mutations = [[config_param['percent_of_mutations_type']],
                           [config_param['percent_of_mutations_rotation']],
                           [config_param['percent_of_mutations_x']],
                           [config_param['percent_of_mutations_y']]]

    game_path = os.path.join(os.path.dirname(project_root), config_param['game_path'])
    write_path = os.path.join(os.path.dirname(project_root),config_param['write_path'])
    read_path = os.path.join(os.path.dirname(project_root),config_param['read_path'])
    log_path = os.path.join(project_root, config_param['log_dir'])
    log_base_name = config_param['log_base_name']


    evolution = ea.Evolution()
    evolution.registerInitialization(initialization=ea.initPopulationDiscretePos)
    evolution.registerFitness(fitness=ea.fitnessPopulationSkip)
    evolution.registerCross(cross=ea.crossSampleNoDuplicate)

    evolution.registerFirstMutation(mutation=ea.mutationBlockType)
    evolution.registerNewMutation(mutation=ea.mutationBlockRotation)
    evolution.registerNewMutation(mutation=ea.mutationBlockPositionX)
    evolution.registerNewMutation(mutation=ea.mutationBlockPositionY)

    evolution.registerReplacement(replacement= ea.elitistReplacement)
    evolution.registerSelection(selection=ea.selectionTournamentNoRepetition)

    max_evaluated = evolution.initEvolution(population_size= population_size, fitness_params=[game_path, write_path, read_path, 0])

    cleanDirectory(write_path)
    cleanDirectory(read_path)
    log_object = {}
    fill = len(str(number_of_generations))
    for generation in range(number_of_generations):
        population, max_evaluated = evolution.runGeneration(fitness_params=[game_path, write_path, read_path, max_evaluated],
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

    end = time.time()
    final_log = {'config': config_param,
                 'execution_time': (end - init),
                 'seed': init,
                 'execution':log_object}
    f = open(os.path.join(project_root, log_path + "/" + log_base_name + timestamp.strftime("_%y%m%d_%H%M%S") + ".json"), 'w')
    json.dump(final_log, f , indent=2)
    xml.writeXML(population[0], os.path.join(project_root, log_path + "/level-0-" +
                                             timestamp.strftime("%y%m%d_%H%M%S") + ".xml"))

if __name__ == "__main__":
    main()
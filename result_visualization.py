#import matplotlib
import json
import os

def last_gen(data, key):
    max_gen = len(data["execution"].items())-1
    fill = len(str(data["config"]["number_of_generations"]))
    return data["execution"][str(max_gen).zfill(fill)][key]

def main():

    times  = []
    best = []
    avg = []
    worst = []
    max_gen = []

    for file_name in os.listdir("./logs"):
        if file_name.endswith(".json") and file_name.startswith("base") and not file_name.startswith("base_large"):
            #print(file_name)
            file = open(os.path.join("./logs", file_name), "r")
            data = json.load(file)

            times.append(data["execution_time"])
            best.append(last_gen(data, "best"))
            avg.append(last_gen(data, "avg"))
            worst.append(last_gen(data, "worst"))
            max_gen.append(len(data["execution"].items()))

    #print(data)

    t = (sum(times)/len(times))
    b = (sum(best)/len(best))
    a = (sum(avg)/len(avg))
    w = (sum(worst)/len(worst))
    g =(sum(max_gen)/len(max_gen))
    print("Experiment 4  & " + str(t/3600) + " (h) & " + str(g) + " & " + str(b) + " & "  + str(a) + " & " + str(w) + " \\\\ \midrule")

if __name__ == '__main__':
    main()
import matplotlib.pyplot as plt
import json
import os
import statistics as st


def plotEvolutionWithSummary(data, name):
    m = max([len(c) for c in data])
    print(m, len(data))
    summary = []
    for i in range(m):
        aux = []
        for c in data:
            if i<len(c):
                aux.append(c[i])
        summary.append(sum(aux)/len(aux))
    # style
    plt.style.use('seaborn-darkgrid')
     
    # create a color palette
    palette = plt.get_cmap('Dark2')
     
    # multiple line plot
    num=0
    for column in data:
        num+=1

        plt.plot(list(range(1, len(column)+1)), column, marker='', color=palette(7), linewidth=1, alpha=0.9)
     
    plt.plot(list(range(1, len(summary)+1)), summary, marker='', color=palette(0), linewidth=3, alpha=0.8, label="average")


    # Add legend
    plt.legend(loc=2, ncol=2)
     
    # Add titles
    plt.title(name, loc='left', fontsize=12, fontweight=0, color=palette(0))
    plt.xlabel("Generation")
    plt.ylabel("Worst fitness")
    plt.show()



def plotEvolution(data, name):
    # style
    plt.style.use('seaborn-darkgrid')
     
    # create a color palette
    palette = plt.get_cmap('Dark2')
     
    # multiple line plot
    num=0
    for column in data:
        num+=1
        plt.plot(list(range(1, len(column)+1)), column, marker='', color=palette(num%8), linewidth=1, alpha=0.9)


    # Add legend
    plt.legend(loc=2, ncol=2)
     
    # Add titles
    plt.title(name, loc='left', fontsize=12, fontweight=0, color=palette(0))
    #plt.xlabel("Generation")
    #plt.ylabel("Best fitness")
    




def scatterPlot(x,y, title):
     # style
    plt.style.use('seaborn-darkgrid')
     
    # create a color palette
    palette = plt.get_cmap('Dark2')

    plt.plot( x, y, linestyle='none', marker='.', color=palette(0))
    plt.title(title, loc='left', fontsize=12, fontweight=0, color=palette(0))
    plt.xlabel("Number of generations")
    plt.ylabel("Solution fitness")
    plt.show()

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
    line_data = []

    for file_name in os.listdir("./logs"):
        #if file_name.endswith(".json") and file_name.startswith("base") and not file_name.startswith("base_large"):
        #if file_name.endswith(".json") and file_name.startswith("base_large"):
        #if file_name.endswith(".json") and file_name.startswith("second_crossover_1") and not file_name.startswith("second_crossover_min"):
        if file_name.endswith(".json") and file_name.startswith("second_crossover_min"):
        #if file_name.endswith(".json") and file_name.startswith("_sim_full"):
        #if file_name.endswith(".json") and file_name.startswith("_sim_sixth"):

            #print(file_name)
            file = open(os.path.join("./logs", file_name), "r")
            data = json.load(file)

            times.append(data["execution_time"])
            best.append(last_gen(data, "best"))
            avg.append(last_gen(data, "avg"))
            worst.append(last_gen(data, "worst"))
            max_gen.append(len(data["execution"].items()))
            l = []
            for k,v in sorted(data["execution"].items()):
                l.append(v["best"])
            line_data.append(l)

    #print(data)

    t = (sum(times)/len(times))
    b = (sum(best)/len(best))
    a = (sum(avg)/len(avg))
    w = (sum(worst)/len(worst))
    g =(sum(max_gen)/len(max_gen))




    print("time  "+str(t)+ "("+str(st.stdev(times))+")") 
    print("best  "+str(b)+ "("+str(st.stdev(best))+")") 
    print("avg   "+str(a)+ "("+str(st.stdev(avg))+")") 
    print("worst "+str(w)+ "("+str(st.stdev(worst))+")") 
    print("ngen  "+str(g)+ "("+str(st.stdev(max_gen))+")") 
    
    #scatterPlot(max_gen, best, "Number of Generations versus fitness of the solution")


    #plotEvolutionWithSummary([x for x in line_data if len(x)< g], "Evolution of the worst individual over generations")
    #plotEvolution([x for x in line_data if len(x)< g/2], "Evolution of the worst individual over generations")
    
    #plt.style.use('seaborn-darkgrid')
    #n, bins, patches =plt.hist(max_gen, bins=[0, 50,150,800])
    #print(n)
    #print(bins)
    #print(patches)
    #plt.show()
    #for i in range(1,len(bins)):
    #    plotdata = [x for x in line_data if bins[i-1]<len(x)< bins[i]]
    #    if len(plotdata) is not 0:
    #        if i == 3 :
    #            plt.subplot2grid( (2,2),(1,0),colspan = 2)
    #            plt.xlabel("Generation")
    #            plt.ylabel("Best fitness")
    #
    #        if i == 1:
    #            plt.ylabel("Best fitness")
    #            plt.subplot2grid( (2,2),(0,0))
    #        if i == 2:
    #            plt.subplot2grid( (2,2),(0,1))
    #        plt.ylim(-10,610)
    #        plotEvolution(plotdata, str(len(plotdata))+" runs, max "+ str(bins[i-1])+ " - " +str(bins[i]))
    #plt.show()


    #print("std of best" + str(st.stdev(best)) )

def  stages_graph():

    file = open(os.path.join("./logs", "second_crossover_min10_verbose_180614_181948.json"), "r")
    data = json.load(file)

    avg = []
    avg_overlapping = []
    avg_distance = []
    avg_broken = []
    avg_base = []
    for k,v in sorted(data["execution"].items()):
        total = v["avg"]
        avg_overlapping.append(v["avg_overlapping_penalty"])
        avg_distance.append(v["avg_distance_penalty"])
        avg_broken.append(v["avg_broken_penalty"])
        avg_base.append(v["avg_base_penalty"])
        avg.append(total)#- avg_overlapping[-1] - avg_distance[-1] - avg_broken[-1]-avg_base[-1])
        
    # style
    plt.style.use('seaborn-darkgrid')
     
    # create a color palette
    palette = plt.get_cmap('Dark2')
    x = list(range(1, len(avg)+1))
    plt.plot(x, avg_overlapping, marker='', color=palette(1), linewidth=1, alpha=0.9, label = "Overlapping Penalty")
    plt.plot(x, avg_distance, marker='', color=palette(2), linewidth=1, alpha=0.9, label="Distance Penalty")
    plt.plot(x, avg_base, marker='', color=palette(4), linewidth=1, alpha=0.9,label="Base Penalty")
    plt.plot(x, avg_broken, marker='', color=palette(3), linewidth=1, alpha=0.9, label="Broken blocks Penalty")
    plt.plot(x, avg, marker='', color=palette(0), linewidth=3, alpha=0.5, label ="Total fitness")

    #plt.stackplot(x, avg_overlapping, avg_distance, avg_base, avg_broken, avg, 
    #    labels=["Overlapping Penalty", "Distance Penalty","Base Penalty", "Broken blocks Penalty", "Total fitness"],
    #    colors=[palette(1),palette(2),palette(4),palette(3),palette(0)]) 
    plt.legend(loc='upper right')
    plt.title("Penalty and fitness distribution over generations", loc='left', fontsize=12, fontweight=0, color=palette(0))
    plt.show()


if __name__ == '__main__':
    main()
import random
import operator

################### make random adjacency matrix for problem ###################
def graph_generator (node):
    adj_graph=[]
    n=node
    for i in range(0,n):
        adj_graph.append([0])
        for j in range(i+1,n):
            adj_graph[i].append(random.randint(0,1))
    print(adj_graph)
    return(adj_graph)

# initialize population (population size =100 and chromosome_size = node_number)#
def initialisation(chromosome,color): 
    pop= dict()
    n=chromosome
    m=color
    for i in range (1,101):
        l=list()
        for j in range(0,n):
            l.append(random.randint(1,m))
        pop[i]=l
        l=[]
    #for obj in list(pop.keys()): #for test initialisation result
     #   print( obj ,pop[obj])
    return(pop)
################### compute fitness for each choromosome ###################
def fittnes_func(graph,node, arr): 
    n=node
    chorom_Arr = arr
    rank=0
    ii = 0
    while ii < n:
        count = ii
        color = chorom_Arr[ii]
        l=ii
        for j in graph[l]:
            if j == 1 and color != chorom_Arr[count]:
                rank +=1000
            elif j == 0:
                rank = rank+10
            count +=1
        ii += 1
    return(rank)

################### selection_roulette wheel  ###################
def selection(fitness): 
    pr=random.uniform(0,0.98)
    select=0
    count = 0
    while select < pr :
        count +=1
        select += fitness[count]
    if count == 100:
        return(count-1)
    else:
        return(count)

################### one point cross over ###################
def crossover_func(l1,l2,len_,graph,clr): 
    n=len_
    point=random.randint(0,n)
    l1[point: ] , l2[point: ] = l2[point: ] , l1[point: ]
    #print(l1,l2) #test new chromosome

    #Mutation
    mutation(l1,n,graph,clr)
    mutation(l2,n,graph,clr)

    return(l1,l2)

################### mutation ###################
def mutation(l1,len__ , graph,clr_): 
    p=random.uniform(0,0.99)
    n=len__
    m=clr_
    if p<0.15:
        j = 0
        while j < n:
            count = j
            color = l1[j]
            l=j
            for j in graph[l]:
                if j == 1 and color == l1[count]:
                    l1[count]= random.randint(1,m)
                    return()       
            j += 1
    else:
        return()

################### compute total fitness for graph ###################
def total_fitness(graph,node): 
    n=node
    counter=0
    total_rank=0
    while counter < n:
        l=counter
        for j in graph[l]:
            if j==1:
                total_rank += 1000
            else:
                total_rank +=10
        counter +=1
    return(total_rank)

######################## main #########################

node_number=int(input('Enter the number of nodes: '))
colors= int(input('Enter the number of colors for coloring: '))
graph = graph_generator(node_number)
population = initialisation(node_number,colors)
total_fit = total_fitness(graph,node_number)

flag = 0
while_count = 1
best_fit={}
while(flag == 0 and while_count < 500):
    fitness={}
    fitness_backup={}
    sum_fit=0
    for chorom in list(population.keys()):
        chorom_Arr = population[chorom]
        fitness[chorom]=fittnes_func(graph,node_number,chorom_Arr)
        fitness_backup[chorom]=fitness[chorom]
    for chorom in list(fitness.keys()):
        sum_fit += fitness[chorom]
    #a=0
    for chorom in list(fitness.keys()):
        fitness[chorom] = fitness[chorom]/sum_fit
        #a = a+ fitness[chorom]
    #print (while_count ,a)
    next_gen=dict()
    i = 50
    j = 101
    while i > 0:
        #selection
        chorom_1=selection(fitness)
        chorom_2=selection(fitness)
        #print(population[chorom_1] , population [chorom_2])

        ################## crossover and Mutation ###################
        child1 , child2 = crossover_func(population[chorom_1], population[chorom_2],node_number,graph,colors)
        population[j]=child1
        population[j+1]=child2
        j += 2
        i -= 1
    
    for chorom in list(population.keys()):
        chorom_Arr = population[chorom]
        fitness_backup[chorom]=fittnes_func(graph,node_number,chorom_Arr)
        if fitness_backup[chorom] == total_fit:
            print('The answer is:')
            print(population[chorom])
            print('Number of cycle: ' , while_count)
            flag =1
            break
    
    if flag==0 :
        #sorted_by_value = sorted(fitness.items(), key=lambda kv: kv[1])
        sorted_fit= sorted(fitness_backup.items(),key=lambda kv: kv[1])
        
        for count in range(0,100):
            del population[sorted_fit[count][0]]
        #if while_count == 1:
        best_fit[sorted_fit[199][1]] = population[sorted_fit[199][0]]
        count = 1
        for chorom in list(population.keys()):
            next_gen[count] = population[chorom]
            count += 1
        population = next_gen
    while_count += 1
sorted_best = sorted(best_fit.items(),key=operator.itemgetter(0))
if while_count == 500 and flag == 0 :
    print("This graph with %i colors in 100 cycle the fitest answer is: " %(colors),)
for fit , chorom in sorted_best:
    print(fit , chorom)
print (total_fit)
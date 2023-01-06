import random
import time
import copy

class KnapsackGenetic:

    def __init__(self, numberOfBoxes, maxWeight, weights, values):
        self.maxWeight = maxWeight
        self.weights = weights
        self.values = values
        self.numberOfBoxes = numberOfBoxes
        self.numberOfPopulation = 100
        self.numberOfAttempts = 100
        self.population= []
        self.populationFitnes = []

    def createInitialPopulation(self):
        number = 0
        while number<self.numberOfPopulation:
            popule = self.createPopule()
            if self.checkValid(popule):
                self.population.append(popule)
                self.populationFitnes.append(self.determiningFitValue(popule))
                number+=1

    def determiningFitValue(self, popule):
        fitnes = 0
        for i in range(len(popule)):
            if popule[i] == 1:
                fitnes+=self.values[i]
        return fitnes
    
    def determiningWaight(self, popule):
        weight = 0
        for i in range(len(popule)):
            if popule[i] == 1:
                weight+=self.weights[i]
        return weight

    def createPopule(self):
        popule = []
        for j in range(self.numberOfBoxes):
            popule.append(random.randint(0, 1))
        return popule

    def checkValid(self, popule):
        if popule in self.population:
            return False
        elif self.determiningWaight(popule)>self.maxWeight:
            return False
        else:
            return True

    def selectParents(self):
        parent1 = self.population[self.populationFitnes.index(max(self.populationFitnes))]
        temp = copy.deepcopy(self.populationFitnes)
        temp.remove(max(temp))
        parent2 = self.population[temp.index(max(temp))]
        return parent1, parent2

    def deleteUselessPeople(self):
        useless = self.population[self.populationFitnes.index(min(self.populationFitnes))]
        self.population.remove(useless)
        self.populationFitnes.remove(min(self.populationFitnes))

    def crossover(self, parent1, parent2):
        child1 = []
        child2 = []
        selection = random.randint(0, self.numberOfBoxes)
        for i in range(self.numberOfBoxes):
            if i<=selection:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child2.append(parent1[i])
                child1.append(parent2[i])
        return child1, child2

    def mutation(self, child):
        selection = random.randint(0, self.numberOfBoxes-1)
        if child[selection] == 1:
            child[selection]=0
        else:
            child[selection]=1
        return child

    def solve(self):
        start = time.time()
        self.createInitialPopulation()
        numberOfAttempt = 0
        oldMaxProfit = max(self.populationFitnes)
        while numberOfAttempt<self.numberOfAttempts:
            parent1, parent2 = self.selectParents()
            child1, child2 = self.crossover(parent1, parent2)
            probabilityOfMutation1 = random.choices(population=[True,False],weights=[0.1,0.9],k=1)
            if probabilityOfMutation1:
                child1 = self.mutation(child1)
            probabilityOfMutation2 = random.choices(population=[True,False],weights=[0.1,0.9],k=1)
            if probabilityOfMutation2:
                child2 = self.mutation(child2)
            if self.checkValid(child1):
                self.deleteUselessPeople()
                self.population.append(child1)
                self.populationFitnes.append(self.determiningFitValue(child1))
            if self.checkValid(child2):
                self.deleteUselessPeople()
                self.population.append(child2)
                self.populationFitnes.append(self.determiningFitValue(child2))
            newMaxProfit = max(self.populationFitnes)
            if oldMaxProfit==newMaxProfit:
                numberOfAttempt+=1
            else:
                oldMaxProfit = newMaxProfit
                numberOfAttempt=0
        end = time.time()
        algoritmTime = end - start
        items = self.population[self.populationFitnes.index(max(self.populationFitnes))]
        selectedItems = []
        boxesWeights = 0
        maxProfit = 0
        for i in range(self.numberOfBoxes):
            if items[i]==1:
                boxesWeights+=weights[i]
                maxProfit+=values[i]
                selectedItems.append(i+1)
        return selectedItems, boxesWeights, maxProfit, algoritmTime
        

def createBoxes():
    maxWeight = int(input("Enter max weight: "))
    weights = []
    values = []
    numberOfBoxes = int(input("Enter number of box: "))
    for i in range(numberOfBoxes):
        weight = int(input("Enter box weight: "))
        weights.append(weight)
        value = int(input("Enter box value: "))
        values.append(value)
    return weights, values, maxWeight, numberOfBoxes

def printResult():
    print("")
    print("selected items: ",selectedItems)
    print("weight: ",boxesWeights)
    print("profit",maxProfit)
    print("time: ",algoritmTime*1000,"ms")

weights, values, maxWeight , numberOfBoxes= createBoxes()
myKnapsackGenetic = KnapsackGenetic(numberOfBoxes, maxWeight, weights, values)

selectedItems, boxesWeights, maxProfit, algoritmTime = myKnapsackGenetic.solve()
printResult()

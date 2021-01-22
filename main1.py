import random, time

MAX_CAPACITY = 10000

STAGE_RECIEVING = 0             #получение зерна
STAGE_CLEANING = 1              #очистка зерна
STAGE_DESINFECTING = 2          #обеззараживание зерна
STAGE_DISPATCHING = 3           #вывоз зерна

NUM_OF_STAGES = 4               #количество процессов
DISPATCH_DELAY = 3              #сколько полных циклов должно пройти чтобы зерно вывезлось

currentStage = STAGE_RECIEVING

recievedGrain = 0
cleanedGrain = 0
goodGrain = 0
badGrain = 0

iters = 0

malfunctions = {'recieving': 1,
                'cleaning': 0,
                'desinfecting': 0,
                'dispatching' : 0,}

#######Funcs#########

def getStage():
    global currentStage
    if currentStage == 0:
        return "Recieving"
    elif currentStage == 1:
        return "Cleaning"
    elif currentStage == 2:
        return "Desinfecting"
    elif currentStage == 3:
        return "Dispatching"


def getStats():
    print("=======",iters,"=======")
    print("Stage: ", getStage())
    print("Recieved grain: ",recievedGrain)
    print("Cleaned grain: ",cleanedGrain)
    print("Good grain: ",goodGrain)
    print("Bad grain: ",badGrain)
    time.sleep(2)


def recieveGrain():
    global recievedGrain
    if malfunctions['recieving'] == 0:
        currentRecieved = random.randint(500,1000)
        if (recievedGrain + currentRecieved < MAX_CAPACITY):
            recievedGrain += currentRecieved
        else:
            print("Error: no more place to storage recieved grain")
    else:
        print("Error: malfunction in recieving storage!")

def cleanGrain():
    global recievedGrain, cleanedGrain
    if malfunctions['cleaning'] == 0:
        currentCleaned = min(600,recievedGrain)
        if (cleanedGrain + currentCleaned < MAX_CAPACITY):
            recievedGrain -= currentCleaned
            cleanedGrain += currentCleaned
        else:
            print("Error: no more place to storage clean grain")
    else:
        print("Error: malfunction in cleaning storage!")

def desinfectGrain():
    global cleanedGrain, goodGrain, badGrain
    if malfunctions['desinfecting'] == 0:
        currentDesinfected = min(500,cleanedGrain)
        badPart = currentDesinfected * round(random.uniform(0.01,0.05),3)  #в процессе может отсеятся от 1.0% до 5.0% зерна
        if (goodGrain + currentDesinfected - badPart < MAX_CAPACITY):
            cleanedGrain -= currentDesinfected
            goodGrain += currentDesinfected - badPart
            badGrain += badPart
        elif (goodGrain + currentDesinfected - badPart > MAX_CAPACITY):
            print("Error: no more place to storage desinfected grain")
        if (badGrain + badPart > MAX_CAPACITY):
            print("Error: no more place to storage bad grain")
    else:
        print("Error: malfunction in recieving storage!")

def dispatchGrain():
    pass
######################


while (True):

    if currentStage == STAGE_RECIEVING:
        recieveGrain()
        getStats()
        currentStage+=1

    if currentStage == STAGE_CLEANING:
        cleanGrain()
        getStats()
        currentStage+=1

    if currentStage == STAGE_DESINFECTING:
        desinfectGrain()
        getStats()
        if iters % DISPATCH_DELAY == 2:
            currentStage+=1
        else:
            currentStage = STAGE_RECIEVING

    if currentStage == STAGE_DISPATCHING:
        dispatchGrain()
        getStats()
        currentStage = STAGE_RECIEVING

    iters += 1

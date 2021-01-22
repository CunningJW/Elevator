import random, time

recievedGrain = 0
cleanedGrain = 0
goodGrain = 0
badGrain = 0

maxCapacity = 10000

STAGE_RECIEVING = 0             #получение зерна
STAGE_CLEANING = 1              #очистка зерна
STAGE_DESINFECTING = 2          #обеззараживание зерна



currentStage = STAGE_RECIEVING

iters = 0




while (True):
    if currentStage == STAGE_RECIEVING:
        currentRecieved = random.randint(500,1000)
        if (recievedGrain + currentRecieved < maxCapacity):
            recievedGrain += currentRecieved
        else:
            pass
        currentStage += 1


    elif currentStage == STAGE_CLEANING:
        currentCleaned = min(600,recievedGrain)
        if (cleanedGrain + currentCleaned < maxCapacity):
            recievedGrain -= currentCleaned
            cleanedGrain += currentCleaned
        else:
            pass
        currentStage += 1

    elif currentStage == STAGE_DESINFECTING:
        currentDesinfected = min(500,cleanedGrain)
        badPart = currentDesinfected * round(random.uniform(0.01,0.05),3)  #в процессе может отсеятся от 1.0% до 5.0% зерна
        if (goodGrain + currentDesinfected - badPart < maxCapacity):
            cleanedGrain -= currentDesinfected
            goodGrain += currentDesinfected - badPart
            badGrain += badPart
        elif (goodGrain + currentDesinfected - badPart > maxCapacity):
            pass
        elif (badGrain + badPart > maxCapacity):
            pass

        currentStage = STAGE_RECIEVING

    iters += 1
    time.sleep(1)

    print("=======",iters,"=======")
    print("Recieved grain: ",recievedGrain)
    print("Cleaned grain: ",cleanedGrain)
    print("Good grain: ",goodGrain)
    print("Bad grain: ",badGrain)

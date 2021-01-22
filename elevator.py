from tkinter import Tk, Canvas, Button, Label
import random, time

MAX_CAPACITY = 10000

STAGE_RECIEVING = 0             #получение зерна
STAGE_CLEANING = 1              #очистка зерна
STAGE_DESINFECTING = 2          #обеззараживание зерна
STAGE_DISPATCHING = 3           #вывоз зерна

NUM_OF_STAGES = 4               #количество процессов
DISPATCH_DELAY = 3              #сколько полных циклов должно пройти чтобы зерно вывезлось

INTERVAL = 1000

currentStage = STAGE_CLEANING

recievedGrain = 10000
cleanedGrain = 0
goodGrain = 0
badGrain = 0

iters = 0


malfunctions = {'recieving': 0,
                'cleaning': 0,
                'desinfecting': 0,
                'dispatching' : 0,}



blinkInterval = 200

window = Tk()
window["bg"] = "snow"
window.resizable(0, 0)

################################# Мигание лампочки ###############################

def fillLightGreen(can, light):
    can.itemconfig(light, fill = "green")
    can.after(blinkInterval, fillLightWhite, can, light)

def fillLightWhite(can, light):
    can.itemconfig(light, fill = "white")
    can.after(blinkInterval, fillLightGreen, can, light)

def blinkLight(can, light):
    fillLightGreen(can, light)

##################################################################################

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

####################################### Лампочки #################################

gettingGrainLightCanvas = Canvas(window, width = 150, height = 30, bg = "snow", highlightthickness = 0)
getCanLight = gettingGrainLightCanvas.create_oval(5, 5, 25, 25, fill = 'white')
gettingGrainLightCanvas.place(x = 0, y = 0)
getGrainText = Label(gettingGrainLightCanvas, text = "Прием зерна", bg = "snow")
getGrainText.place(x = 30, y = 5)

cleaningGrainLightCanvas = Canvas(window, width = 150, height = 30, bg = "snow", highlightthickness = 0)
cleanCanLight = cleaningGrainLightCanvas.create_oval(5, 5, 25, 25, fill = 'white')
cleaningGrainLightCanvas.place(x = 0, y = 30)
cleanGrainText = Label(cleaningGrainLightCanvas, text = "Очистка зерна", bg = "snow")
cleanGrainText.place(x = 30, y = 5)

disinfectionGrainLightCanvas = Canvas(window, width = 200, height = 30, bg = "snow", highlightthickness = 0)
disinfectionCanLight = disinfectionGrainLightCanvas.create_oval(5, 5, 25, 25, fill = 'white')
disinfectionGrainLightCanvas.place(x = 0, y = 60)
disinfectionGrainText = Label(disinfectionGrainLightCanvas, text = "Обеззараживание зерна", bg = "snow")
disinfectionGrainText.place(x = 30, y = 5)

##################################################################################

########################## Смещение стрелочки по x и y ##########################

def arrowMove(massiv, x, y):
    for i in range(len(massiv)):
        if i % 2 == 0:
            massiv[i] += x
        else:
            massiv[i] += y
    return massiv

##################################################################################

##################################### Мигание стрелочки ##########################

def changeObjectColor(can,color,object):
    can.itemconfig(object, fill = color)

def blinkArrow(can, arrows):
    for arrow in arrows:
        interval = 0
        for i in range(round(INTERVAL/blinkInterval)):
            if i % 2:
                can.after(interval,changeObjectColor,can,'green',arrow)
            else:
                can.after(interval,changeObjectColor,can,'white',arrow)
            interval += blinkInterval
        can.after(INTERVAL,changeObjectColor,can,'white',arrow)
##################################################################################

####################################### Элеватор #################################

arrowCoordinates = [
                    105, 150,
                    135, 150,
                    135, 145,
                    155, 155,
                    135, 165,
                    135, 160,
                    105, 160,
                             ]

elevatorCanvas = Canvas(window, width = 720, height = 300, bg = "snow", highlightthickness = 0)
elevatorCanvas.place(x = 560, y = 0)

gettinGraingBox = elevatorCanvas.create_rectangle(10, 30, 100, 280)
getGrainBoxText = Label(elevatorCanvas, text = "Принятое зерно", bg = "snow")
getGrainBoxText.place(x = 8, y = 5)

getToCleanArrow = elevatorCanvas.create_polygon(arrowCoordinates, fill = "snow", outline = "black")

cleaningGrainBox = elevatorCanvas.create_rectangle(160, 30, 250, 280)
cleanGrainBoxText = Label(elevatorCanvas, text = "Очищенное зерно", bg = "snow")
cleanGrainBoxText.place(x = 152, y = 5)

disinfectionToGoodGrainArrow = elevatorCanvas.create_polygon(arrowMove(arrowCoordinates, 150, -75), fill = "snow", outline = "black")
disinfectionToBadGrainArrow = elevatorCanvas.create_polygon(arrowMove(arrowCoordinates, 0, 150), fill = "snow", outline = "black")

goodGrainBox = elevatorCanvas.create_rectangle(310, 30, 560, 130)
goodGrainBoxText = Label(elevatorCanvas, text = "Хорошее зерно", bg = "snow")
goodGrainBoxText.place(x = 396, y = 5)

badGrainBox = elevatorCanvas.create_rectangle(310, 180, 560, 280)
badGrainBoxText = Label(elevatorCanvas, text = "Плохое зерно", bg = "snow")
badGrainBoxText.place(x = 400, y = 155)

##################################################################################


def progress():
    global currentStage, iters

    if currentStage == STAGE_CLEANING:
        iters += 1
        cleanGrain()
        getStats()
        if (recievedGrain != 0):
            blinkArrow(elevatorCanvas, [getToCleanArrow])
        currentStage+=1
        elevatorCanvas.after(INTERVAL,progress)

    elif currentStage == STAGE_DESINFECTING:
        desinfectGrain()
        getStats()
        if (cleanedGrain != 0):
            blinkArrow(elevatorCanvas, [disinfectionToGoodGrainArrow])
            blinkArrow(elevatorCanvas, [disinfectionToBadGrainArrow])
        if iters % DISPATCH_DELAY == 0:                                 #когда проходит нужное количество дней до отправки
            currentStage+=1                                             #сначала отправляем зерно, а потом начинаем новый цикл
            elevatorCanvas.after(INTERVAL,progress)
        else:                                                           #иначе начинаем новый цикл сразу
            currentStage = STAGE_CLEANING
            elevatorCanvas.after(INTERVAL,progress)

    elif currentStage == STAGE_DISPATCHING:
        dispatchGrain()
        getStats()
        currentStage = STAGE_CLEANING
        elevatorCanvas.after(INTERVAL,progress)

##################################################################################
elevatorCanvas.after(0,progress)
window.geometry('1280x720')
window.mainloop()

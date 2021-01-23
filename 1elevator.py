from tkinter import Tk, Canvas, Button, Label, Entry
import random, time, math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

MAX_CAPACITY = 10000            #максимум кг зерна

STAGE_RECIEVING = 0             #получение зерна
STAGE_CLEANING = 1              #очистка зерна
STAGE_DESINFECTING = 2          #обеззараживание зерна
STAGE_DISPATCHING = 3           #вывоз зерна

NUM_OF_STAGES = 4               #количество процессов
DISPATCH_DELAY = 3              #сколько полных циклов должно пройти чтобы зерно вывезлось

INTERVAL = 1000

grainKgCost = 20                #стоймость (р/кг)
exportAmount = 500


currentStage = STAGE_CLEANING

recievedGrain = 10000
cleanedGrain = 0
goodGrain = 0
badGrain = 0

iters = 0


malfunctions = {'recieving': False,
                'cleaning': False,
                'desinfecting': False,
                'dispatching' : False,}


totalIncome = 0   #доходы
totalExpense = 0  #расходы
totalProfit = 0   #прибыль
kek = [[0.0,0.0]]


blinkInterval = 200

window = Tk()
window["bg"] = "snow"
window.resizable(0, 0)



fig = plt.figure(figsize = (5,4),frameon = False)
fig.patch.set_facecolor('snow')
ax1 = fig.add_subplot(1, 1, 1)


######################################Funcs#######################################

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

def recieveGrain(event):
    global recievedGrain
    if malfunctions['recieving'] == False:
        currentRecieved = 1000
        if (recievedGrain + currentRecieved < MAX_CAPACITY):
            recievedGrain += currentRecieved
            getGrainAmountText.config(text = "{0} / {1}".format(recievedGrain, MAX_CAPACITY))
            fillBox(elevatorCanvas, gettinGraingBox, math.floor(recievedGrain / MAX_CAPACITY * 100))
        else:
            print("Error: no more place to storage recieved grain")
    else:
        print("Error: malfunction in recieving storage!")

def cleanGrain():
    global recievedGrain, cleanedGrain
    if malfunctions['cleaning'] == False:
        currentCleaned = min(600,recievedGrain)
        if (cleanedGrain + currentCleaned < MAX_CAPACITY):
            recievedGrain -= currentCleaned
            cleanedGrain += currentCleaned
            getGrainAmountText.config(text = "{0} / {1}".format(recievedGrain, MAX_CAPACITY))
            cleaningGrainAmountText.config(text = "{0} / {1}".format(cleanedGrain, MAX_CAPACITY))
            fillBox(elevatorCanvas, gettinGraingBox, math.floor(recievedGrain / MAX_CAPACITY * 100))
            fillBox(elevatorCanvas, cleaningGrainBox, math.floor(cleanedGrain / MAX_CAPACITY * 100))
        else:
            print("Error: no more place to storage clean grain")
    else:

        print("Error: malfunction in cleaning storage!")

def desinfectGrain():
    global cleanedGrain, goodGrain, badGrain
    if malfunctions['desinfecting'] == False:
        currentDesinfected = min(500,cleanedGrain)
        badPart = currentDesinfected * round(random.uniform(0.01,0.05),3)  #в процессе может отсеятся от 1.0% до 5.0% зерна
        if (goodGrain + currentDesinfected - badPart < MAX_CAPACITY):
            cleanedGrain -= currentDesinfected
            goodGrain += currentDesinfected - badPart
            badGrain += badPart
            cleaningGrainAmountText.config(text = "{0} / {1}".format(cleanedGrain, MAX_CAPACITY))
            goodGrainAmountText.config(text = "{0} / {1}".format(goodGrain, MAX_CAPACITY))
            badGrainAmountText.config(text = "{0} / 500".format(badGrain))
            fillBox(elevatorCanvas, cleaningGrainBox, math.floor(cleanedGrain / MAX_CAPACITY * 100))
            fillBox(elevatorCanvas, goodGrainBox, math.floor(goodGrain / MAX_CAPACITY * 100))
            fillBox(elevatorCanvas, badGrainBox, math.floor(badGrain / 500 * 100))
        elif (goodGrain + currentDesinfected - badPart > MAX_CAPACITY):
            print("Error: no more place to storage desinfected grain")
        if (badGrain + badPart > 500):
            print("Error: no more place to storage bad grain")
    else:
        print("Error: malfunction in recieving storage!")

def dispatchGrain():
    global goodGrain, totalIncome, exportAmount
    if malfunctions['dispatching'] == False:
        currentDispatched = min(goodGrain,exportAmount)
        goodGrain -= currentDispatched
        totalIncome += currentDispatched * grainKgCost
##################################################################################

# Смещение стрелочки по x и y #
def arrowMove(massiv, x, y):
    for i in range(len(massiv)):
        if i % 2 == 0:
            massiv[i] += x
        else:
            massiv[i] += y
    return massiv

# Мигание стрелочки #

def changeObjectColor(can,color,object):
    can.itemconfig(object, fill = color)

def blinkArrow(can, arrows, color):
    for arrow in arrows:
        interval = 0
        for i in range(round(INTERVAL/blinkInterval)):
            if i % 2:
                can.after(interval, changeObjectColor, can, color, arrow)
            else:
                can.after(interval, changeObjectColor, can, 'white', arrow)
            interval += blinkInterval
        can.after(INTERVAL, changeObjectColor, can, 'white', arrow)


# Заполнение склада #

massivBox = []

def fillBox(can, box, percent):   #Нужно указать канвас в котором находится нужный прямоугольник, сам прямоугольник и процент заполнение (0-100)
    global massivBox
    k = 0
    coordsBox = can.coords(box)

    if len(massivBox) == 0:
        fillingBox = can.create_rectangle(coordsBox[0],coordsBox[3],coordsBox[2],coordsBox[3], fill = "wheat")
        massivBox.append(fillingBox)

    for i in range(len(massivBox)):
        coordsFillingBox = can.coords(massivBox[i])
        if coordsFillingBox[0] == coordsBox[0] and coordsFillingBox[3] == coordsBox[3]:
            j = i
            k = 1
            break

    if k == 0:
        fillingBox = can.create_rectangle(coordsBox[0],coordsBox[3],coordsBox[2],coordsBox[3], fill = "wheat")
        massivBox.append(fillingBox)
    else:
        height = percent * (coordsBox[3] - coordsBox[1]) / 100 # учитывает высоту заполнения относительно высоты самого прямоугольника
        coordsBox[1] = coordsBox[3] - height #изменяем координату y левого верхнего угла прямоугольника, оставляя все остальные координаты неизменными
        can.coords(massivBox[j],coordsBox) #

def clearBadBox(event):
    global totalExpense, badGrain
    blinkArrow(elevatorCanvas, [badGrainArrowToExport], "green")
    totalExpense += 10000 + badGrain
    badGrain = 0
    fillBox(elevatorCanvas, badGrainBox, 0)

def numberGoodExport(event):
    global exportAmount
    exportAmount = float(numberGoodExportInput.get())
#####################

##########################Стрелки, боксы и названия###############################

arrowCoordinates = [
                    105, 150,
                    135, 150,
                    135, 145,
                    155, 155,
                    135, 165,
                    135, 160,
                    105, 160,
                             ]

elevatorCanvas = Canvas(window, width = 780, height = 300, bg = "snow", highlightthickness = 0)
elevatorCanvas.place(x = 500, y = 0)

gettinGraingBox = elevatorCanvas.create_rectangle(10, 30, 100, 280)
getGrainBoxText = Label(elevatorCanvas, text = "Принятое зерно", bg = "snow")
getGrainBoxText.place(x = 8, y = 5)

getToCleanArrow = elevatorCanvas.create_polygon(arrowCoordinates, fill = "snow", outline = "black")

getGrainAmountText = Label(elevatorCanvas, text = "{0} / {1}".format(recievedGrain, MAX_CAPACITY), width = 10, bg = "snow")
getGrainAmountText.place(x = 15, y = 285)

cleaningGrainBox = elevatorCanvas.create_rectangle(160, 30, 250, 280)
cleanGrainBoxText = Label(elevatorCanvas, text = "Очищенное зерно", bg = "snow")
cleanGrainBoxText.place(x = 152, y = 5)

cleaningGrainAmountText = Label(elevatorCanvas, text = "{0} / {1}".format(cleanedGrain, MAX_CAPACITY), width = 10, bg = "snow")
cleaningGrainAmountText.place(x = 168, y = 285)

disinfectionToGoodGrainArrow = elevatorCanvas.create_polygon(arrowMove(arrowCoordinates, 150, -75), fill = "snow", outline = "black")
disinfectionToBadGrainArrow = elevatorCanvas.create_polygon(arrowMove(arrowCoordinates, 0, 150), fill = "snow", outline = "black")

goodGrainBox = elevatorCanvas.create_rectangle(310, 30, 560, 130)
goodGrainBoxText = Label(elevatorCanvas, text = "Хорошее зерно", bg = "snow")
goodGrainBoxText.place(x = 396, y = 5)

goodGrainAmountText = Label(elevatorCanvas, text = "{0} / {1}".format(goodGrain, MAX_CAPACITY), width = 10, bg = "snow")
goodGrainAmountText.place(x = 405, y = 135)

badGrainBox = elevatorCanvas.create_rectangle(310, 180, 560, 280)
badGrainBoxText = Label(elevatorCanvas, text = "Плохое зерно", bg = "snow")
badGrainBoxText.place(x = 400, y = 155)

badGrainAmountText = Label(elevatorCanvas, text = "{0} / 500".format(badGrain), width = 8, bg = "snow")
badGrainAmountText.place(x = 405, y = 285)

goodGrainArrowToExport = elevatorCanvas.create_polygon(arrowMove(arrowCoordinates, 310, -150), fill = "snow", outline = "black")
badGrainArrowToExport = elevatorCanvas.create_polygon(arrowMove(arrowCoordinates, 0, 150), fill = "snow", outline = "black")

goodExportBox = elevatorCanvas.create_rectangle(620, 30, 750, 130)
goodExportBoxText = Label(elevatorCanvas, text = "Вывоз", bg = "snow")
goodExportBoxText.place(x = 666, y = 5)


timeGoodExportText = Label(elevatorCanvas, text = "Через дней", bg = "snow")
timeGoodExportText.place(x = 625, y = 35)

numberGoodExportText1 = Label(elevatorCanvas, text = "Кол-во:", bg = "snow")
numberGoodExportText1.place(x = 625, y = 100)

numberGoodExportInput = Entry(elevatorCanvas, width = 5)
numberGoodExportInput.insert(0, str(exportAmount))
numberGoodExportInput.place(x = 675, y = 100)

numberGoodExportButtonCanvas = Canvas(elevatorCanvas, width = 5, height = 5)
numberGoodExportButtonCanvas.place(x = 712, y = 98)

numberGoodExportButton = Button(numberGoodExportButtonCanvas, text = "Add", width = 2, height = 1, bg = "Black",foreground = "white")
numberGoodExportButton.pack(side = "top")
numberGoodExportButton.bind(sequence = "<Button-1>", func = numberGoodExport)

badExportButtonCanvas = Canvas(elevatorCanvas, width = 150, height = 10)
badExportButtonCanvas.place(x = 625, y = 218)

badExportButton = Button(badExportButtonCanvas, text = "Очистка", width = 20, height = 1, bg = "Black",foreground = "white")
badExportButton.pack(side = "top")
badExportButton.bind(sequence = "<Button-1>", func = clearBadBox)

#################################################################################

################################ График #########################################

def drawGraph(kek):
    xs = []
    ys = []
    for line in kek:
        xs.append(line[0])
        ys.append(line[1])

    ax1.clear()
    ax1.plot(xs, ys)

    ax1.set_xlabel('Days')
    ax1.set_ylabel('Profit')
    ax1.set_title('Profit over time graph')

    fig.canvas.draw()

#################################################################################

################################ Кнопки #########################################

canButton = Canvas(window, width = 20, height = 20)
canButton.place(x = 10, y = 200)

errorText = Label(window, text = "", bg = "snow")
errorText.place(x = 10, y = 250)

addGrainButton = Button(canButton, text = "Add 1000 Grain", width = 25, height = 2, bg = "Black",foreground = "white")
addGrainButton.pack(side = "left")
addGrainButton.bind(sequence = "<Button-1>", func = recieveGrain)

#################################################################################

def progress():
    global currentStage, iters, totalIncome, totalExpense, totalProfit

    if currentStage == STAGE_CLEANING:
        iters += 1
        cleanGrain()
        getStats()

        if (recievedGrain != 0):
            blinkArrow(elevatorCanvas, [getToCleanArrow], "green")
        currentStage+=1
        elevatorCanvas.after(INTERVAL,progress)

    elif currentStage == STAGE_DESINFECTING:
        desinfectGrain()
        getStats()
        if (cleanedGrain != 0):
            blinkArrow(elevatorCanvas, [disinfectionToGoodGrainArrow,
                                        disinfectionToBadGrainArrow], "green")
        if iters % DISPATCH_DELAY == 0:                                 #когда проходит нужное количество дней до отправки
            currentStage+=1
            print(kek)                                          #сначала отправляем зерно, а потом начинаем новый цикл
            drawGraph(kek)
            elevatorCanvas.after(INTERVAL,progress)
        else:                                                           #иначе начинаем новый цикл сразу
            currentStage = STAGE_CLEANING
            drawGraph(kek)
            elevatorCanvas.after(INTERVAL,progress)


    elif currentStage == STAGE_DISPATCHING:
        dispatchGrain()
        getStats()
        blinkArrow(elevatorCanvas, [goodGrainArrowToExport], "green")
        currentStage = STAGE_CLEANING
        elevatorCanvas.after(INTERVAL,progress)



    totalExpense += 500
    totalProfit = totalIncome - totalExpense

    if (iters == kek[(len(kek)-1)][0]):
        kek[(len(kek) - 1)] = [iters,totalProfit]
    else:
        kek.append([iters,totalProfit])

    if len(kek) > 15:               #максимальный размер массива
        del kek[0]

    print(totalIncome)
    print(totalExpense)
    print(totalProfit)

    timeGoodExportText.config(text = "Через {0} дн.".format(str(abs(iters % DISPATCH_DELAY % (-1*DISPATCH_DELAY)))))
    print()
##################################################################################

canGraph = Canvas(window, width = 800, height = 600)
canGraph.place(x = 780, y = 300)
canvasGraph = FigureCanvasTkAgg(fig, canGraph)
canvasGraph.get_tk_widget().config(bg = 'snow')
canvasGraph.get_tk_widget().grid(column=0,row=0)

elevatorCanvas.after(0,progress)
window.geometry('1280x720')
window.mainloop()

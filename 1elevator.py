from tkinter import Tk, Canvas, Button, Label, Entry, messagebox
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
taxeGrain = 0
flag = 0

malfunctions = {'recieving': False,
                'cleaning': False,
                'desinfecting': False,
                'dispatching' : False,}


totalIncome = 0   #доходы
totalExpense = 0  #расходы
totalProfit = 0   #прибыль

currentIncome = 0   #текущие доходы
currentExpense = 0  #текущие расходы
currentProfit = 0   #текущая прибыль

taxes = 1000 #плата за обслуживание

kek = [[0.0,0.0]]
profitTable = [ ['','','','','','','',''] for i in range(10) ]

blinkInterval = 200

window = Tk()
window["bg"] = "snow"
window.resizable(0, 0)



fig = plt.figure(figsize = (7,4),frameon = False)
fig.patch.set_facecolor('snow')
ax1 = fig.add_subplot(1, 1, 1)

tableFig = plt.figure(figsize = (8,4.5),frameon = False)
tableFig.patch.set_facecolor('snow')
tableFig.patch.set_visible(False)
ax2 = tableFig.add_subplot()

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
    print("")

def recieveGrain(event):
    global recievedGrain, currentProfit, currentExpense, flag
    currentIncome = 0
    currentExpense = taxes
    currentProfit = currentIncome - currentExpense
    if malfunctions['recieving'] == False:
        currentRecieved = 1000
        if (recievedGrain + currentRecieved < MAX_CAPACITY):
            recievedGrain += currentRecieved
            getGrainAmountText.config(text = "{0} / {1} kg".format(recievedGrain, MAX_CAPACITY))
            fillBox(elevatorCanvas, gettinGraingBox, math.floor(recievedGrain / MAX_CAPACITY * 100))
        else:
            print("Error: no more place to storage recieved grain")
    else:
        print("Error: malfunction in recieving storage!")
    if flag == 1:
        flag = 0
        currentExpense += 10000 + taxeGrain
        currentProfit -= currentExpense
    elif flag == 2:
        flag = 0
        currentExpense += 500
        currentProfit -= currentExpense

def cleanGrain():
    global recievedGrain, cleanedGrain, currentProfit, currentExpense, currentIncome, flag
    currentIncome = 0
    currentExpense = taxes
    currentProfit = currentIncome - currentExpense
    if malfunctions['cleaning'] == False:
        currentCleaned = min(600,recievedGrain)
        if (cleanedGrain + currentCleaned < MAX_CAPACITY):
            recievedGrain -= currentCleaned
            cleanedGrain += currentCleaned
            getGrainAmountText.config(text = "{0} / {1} kg".format(recievedGrain, MAX_CAPACITY))
            cleaningGrainAmountText.config(text = "{0} / {1} kg".format(cleanedGrain, MAX_CAPACITY))
            fillBox(elevatorCanvas, gettinGraingBox, math.floor(recievedGrain / MAX_CAPACITY * 100))
            fillBox(elevatorCanvas, cleaningGrainBox, math.floor(cleanedGrain / MAX_CAPACITY * 100))
        else:
            print("Error: no more place to storage clean grain")
    else:
        print("Error: malfunction in cleaning storage!")
    if flag == 1:
        flag = 0
        currentExpense += 10000 + taxeGrain
        currentProfit -= currentExpense
    elif flag == 2:
        flag = 0
        currentExpense += 500
        currentProfit -= currentExpense

def desinfectGrain():
    global cleanedGrain, goodGrain, badGrain, currentProfit, currentExpense, currentIncome, flag
    currentIncome = 0
    currentExpense = taxes
    currentProfit = currentIncome - currentExpense
    if malfunctions['desinfecting'] == False:
        currentDesinfected = min(500,cleanedGrain)
        badPart = currentDesinfected * round(random.uniform(0.01,0.05),3)  #в процессе может отсеятся от 1.0% до 5.0% зерна
        if (goodGrain + currentDesinfected - badPart < MAX_CAPACITY):
            cleanedGrain -= currentDesinfected
            goodGrain += currentDesinfected - badPart
            badGrain += badPart
            cleaningGrainAmountText.config(text = "{0} / {1} kg".format(cleanedGrain, MAX_CAPACITY))
            goodGrainAmountText.config(text = "{0} / {1} kg".format(goodGrain, MAX_CAPACITY))
            badGrainAmountText.config(text = "{0} / 500 kg".format(badGrain))
            fillBox(elevatorCanvas, cleaningGrainBox, math.floor(cleanedGrain / MAX_CAPACITY * 100))
            fillBox(elevatorCanvas, goodGrainBox, math.floor(goodGrain / MAX_CAPACITY * 100))
            fillBox(elevatorCanvas, badGrainBox, math.floor(badGrain / 500 * 100))
        elif (goodGrain + currentDesinfected - badPart > MAX_CAPACITY):
            print("Error: no more place to storage desinfected grain")
        if (badGrain + badPart > 500):
            print("Error: no more place to storage bad grain")
    else:
        print("Error: malfunction in recieving storage!")
    if flag == 1:
        flag = 0
        currentExpense += 10000 + taxeGrain
        currentProfit -= currentExpense
    elif flag == 2:
        flag = 0
        currentExpense += 500
        currentProfit -= currentExpense
def dispatchGrain():
    global goodGrain, exportAmount, currentProfit, currentExpense, currentIncome, flag, taxeGrain
    if malfunctions['dispatching'] == False:
        currentDispatched = min(goodGrain,exportAmount)
        goodGrain -= currentDispatched
        currentIncome += currentDispatched * grainKgCost
        currentExpense += taxes
        currentProfit += currentIncome - currentExpense
    if flag == 1:
        flag = 0
        currentExpense = 10000 + taxeGrain
        currentProfit = currentExpense
    elif flag == 2:
        flag = 0
        currentExpense += 500
        currentProfit -= currentExpense

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
    global totalExpense, badGrain, currentExpense, currentProfit, flag, taxeGrain
    blinkArrow(elevatorCanvas, [badGrainArrowToExport], "green")
    flag = 1
    taxeGrain = badGrain
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

canvasLabel = Canvas(window, width = 150, height = 50, bg = 'snow')

totalIncomeText = Label(canvasLabel, text = currentIncome, font=("arial", 10), bg="snow", anchor = "w", width=30)
totalExpenceText = Label(canvasLabel, text = currentExpense, font=("arial", 10), bg="snow", anchor = "w", width=30)
totalProfitText = Label(canvasLabel, text = currentProfit, font=("arial", 10), bg="snow", anchor = "w", width=30)


totalIncomeText.grid(row = 0,column = 0)
totalExpenceText.grid(row = 1,column = 0)
totalProfitText.grid(row = 2,column = 0)

canvasLabel.place(x = 0, y = 10)

elevatorCanvas = Canvas(window, width = 780, height = 305, bg = "snow", highlightthickness = 0)
elevatorCanvas.place(x = 500, y = 0)

gettinGrainButtonCanvas = Canvas(window, width = 150, height = 10)
gettinGrainButtonCanvas.place(x = 350, y = 135)

gettinGrainButton = Button(gettinGrainButtonCanvas, text = "Add 1000 Grain", width = 20, height = 2, bg = "Black",foreground = "white")
gettinGrainButton.pack(side = "left")
gettinGrainButton.bind(sequence = "<Button-1>", func = recieveGrain)

gettinGraingBox = elevatorCanvas.create_rectangle(10, 30, 100, 280)
getGrainBoxText = Label(elevatorCanvas, text = "Принятое зерно", bg = "snow")
getGrainBoxText.place(x = 8, y = 5)

getToCleanArrow = elevatorCanvas.create_polygon(arrowCoordinates, fill = "snow", outline = "black")

getGrainAmountText = Label(elevatorCanvas, text = "{0} / {1} kg".format(recievedGrain, MAX_CAPACITY), width = 12, bg = "snow")
getGrainAmountText.place(x = 15, y = 285)

cleaningGrainBox = elevatorCanvas.create_rectangle(160, 30, 250, 280)
cleanGrainBoxText = Label(elevatorCanvas, text = "Очищенное зерно", bg = "snow")
cleanGrainBoxText.place(x = 152, y = 5)

cleaningGrainAmountText = Label(elevatorCanvas, text = "{0} / {1} kg".format(cleanedGrain, MAX_CAPACITY), width = 12, bg = "snow")
cleaningGrainAmountText.place(x = 168, y = 285)

desinfectionToGoodGrainArrow = elevatorCanvas.create_polygon(arrowMove(arrowCoordinates, 150, -75), fill = "snow", outline = "black")
desinfectionToBadGrainArrow = elevatorCanvas.create_polygon(arrowMove(arrowCoordinates, 0, 150), fill = "snow", outline = "black")

goodGrainBox = elevatorCanvas.create_rectangle(310, 30, 560, 130)
goodGrainBoxText = Label(elevatorCanvas, text = "Хорошее зерно", bg = "snow")
goodGrainBoxText.place(x = 396, y = 5)

goodGrainAmountText = Label(elevatorCanvas, text = "{0} / {1} kg".format(goodGrain, MAX_CAPACITY), width = 12, bg = "snow")
goodGrainAmountText.place(x = 405, y = 135)

badGrainBox = elevatorCanvas.create_rectangle(310, 180, 560, 280)
badGrainBoxText = Label(elevatorCanvas, text = "Плохое зерно", bg = "snow")
badGrainBoxText.place(x = 400, y = 155)

badGrainAmountText = Label(elevatorCanvas, text = "{0} / 500 kg".format(badGrain), width = 10, bg = "snow")
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

################################ График и таблица #########################################

def drawGraph(kek):
    xs = []
    ys = []
    for line in kek[:len(kek) - 1]:
        xs.append(line[0])
        ys.append(line[1])

    ax1.clear()
    ax1.plot(xs, ys)

    ax1.set_xlabel('Days')
    ax1.set_ylabel('Profit')
    ax1.set_title('Profit over time graph')

    fig.canvas.draw()

def drawTable(profitTable):
    ax2.clear()
    ax2.table(cellText = profitTable[::-1],
              colLabels = ['Days','Income($)','Expense($)','Profit($)','Recieved Grain', 'Cleaned Grain', 'Good Grain', 'Bad Grain'],
              loc='center',
              bbox=[0,0,1.1,1.1],
              colWidths = [0.3,0.5,0.5,0.4,0.7,0.7,0.6,0.6],
              )
    ax2.axis('off')
    ax2.axis('tight')
    tableFig.canvas.draw()
#################################################################################
def breakingCleaning(event):
    global malfunctions
    malfunctions['cleaning'] = True

def repairingCleaning(event):
    global malfunctions
    malfunctions['cleaning'] = False

def breakingDesinfecting(event):
    global malfunctions
    malfunctions['desinfecting'] = True

def repairingDesinfecting(event):
    global malfunctions
    malfunctions['desinfecting'] = False

def breakingDispatching(event):
    global malfunctions
    malfunctions['dispatching'] = True

def repairingDispatching(event):
    global malfunctions
    malfunctions['dispatching'] = False

def makeError(event):
    global flag
    flag = 3
def syserror():
        global flag
        messagebox.showerror(
            "System malfunction",
            "Press OK to fix system (500$)")
        flag = 2
################################ Кнопки #########################################

canButtons = Canvas(window, width = 300, height = 250, bg = "snow", highlightthickness = 0)
canButtons.place(x = 0, y = 100)

canCleaningButton = Canvas(canButtons, width = 300, height = 1, bg = "snow", highlightthickness = 0)
canCleaningButton.place(x = 0, y = 0)

canDesinfectingButton = Canvas(canButtons, width = 300, height = 1, bg = "snow", highlightthickness = 0)
canDesinfectingButton.place(x = 0, y = 50)

canDispatchingingButton = Canvas(canButtons, width = 300, height = 1, bg = "snow", highlightthickness = 0)
canDispatchingingButton.place(x = 0, y = 100)

breakingCleaningButton = Button(canCleaningButton, text = "Очистка не работает", width = 20, height = 1, bg = "Black",foreground = "white")
breakingCleaningButton.pack(side = 'left')
breakingCleaningButton.bind(sequence = "<Button-1>", func = breakingCleaning)

repairingCleaningButton = Button(canCleaningButton, text = "Очистка работает", width = 20, height = 1, bg = "Black",foreground = "white")
repairingCleaningButton.pack(side = 'right')
repairingCleaningButton.bind(sequence = "<Button-1>", func = repairingCleaning)

breakingDesinfectingButton = Button(canDesinfectingButton, text = "Дизенфекция не работает", width = 20, height = 1, bg = "Black",foreground = "white")
breakingDesinfectingButton.pack(side = 'left')
breakingDesinfectingButton.bind(sequence = "<Button-1>", func = breakingDesinfecting)

repairingDesinfectingButton = Button(canDesinfectingButton, text = "Дизенфекция работает", width = 20, height = 1, bg = "Black",foreground = "white")
repairingDesinfectingButton.pack(side = 'right')
repairingDesinfectingButton.bind(sequence = "<Button-1>", func = repairingDesinfecting)

breakingDispatchingButton = Button(canDispatchingingButton, text = "Отправка не работает", width = 20, height = 1, bg = "Black",foreground = "white")
breakingDispatchingButton.pack(side = 'left')
breakingDispatchingButton.bind(sequence = "<Button-1>", func = breakingDispatching)

repairingDispatchingButton = Button(canDispatchingingButton, text = "Отправка работает", width = 20, height = 1, bg = "Black",foreground = "white")
repairingDispatchingButton.pack(side = 'right')
repairingDispatchingButton.bind(sequence = "<Button-1>", func = repairingDispatching)

canStopSystemButton = Canvas(window, width = 200, height = 300, bg = "snow", highlightthickness = 0)
canStopSystemButton.place(x = 1300, y = 125)

stopSystemButton = Button(canStopSystemButton, text = 'System \n Stop', width = 10, height = 2, bg = "red",foreground = "white")
stopSystemButton.pack(side = 'bottom')
stopSystemButton.bind(sequence="<Button-1>", func = makeError)
#################################################################################

def progress():
    global currentStage, iters, totalIncome, totalExpense, totalProfit, goodGrain, badGrain, flag
    if flag == 3:
        syserror()
        flag = 2
        elevatorCanvas.after(INTERVAL,progress)
    else:
        if currentStage == STAGE_CLEANING:
            iters += 1
            cleanGrain()
            getStats()

            if (recievedGrain != 0):
                if malfunctions['cleaning'] == False:
                    blinkArrow(elevatorCanvas, [getToCleanArrow], "green")
                else:
                    blinkArrow(elevatorCanvas, [getToCleanArrow], "red")
            currentStage+=1
            elevatorCanvas.after(INTERVAL,progress)

        elif currentStage == STAGE_DESINFECTING:
            desinfectGrain()
            getStats()
            if (cleanedGrain != 0):
                if malfunctions['desinfecting'] == False:
                    blinkArrow(elevatorCanvas, [desinfectionToGoodGrainArrow,
                                                desinfectionToBadGrainArrow], "green")
                else:
                    blinkArrow(elevatorCanvas, [desinfectionToGoodGrainArrow,
                                                desinfectionToBadGrainArrow], "red")
            if iters % DISPATCH_DELAY == 0:                                 #когда проходит нужное количество дней до отправки
                currentStage+=1
                elevatorCanvas.after(INTERVAL,progress)
            else:                                                           #иначе начинаем новый цикл сразу
                currentStage = STAGE_CLEANING
                profitTable.append([iters, currentIncome, currentExpense, currentProfit, recievedGrain, cleanedGrain, round(goodGrain, 1) , round(badGrain, 1)])
                elevatorCanvas.after(INTERVAL,progress)


        elif currentStage == STAGE_DISPATCHING:
            dispatchGrain()
            getStats()
            if malfunctions['dispatching'] == False:
                blinkArrow(elevatorCanvas, [goodGrainArrowToExport], "green")
            else:
                blinkArrow(elevatorCanvas, [goodGrainArrowToExport], "red")
            currentStage = STAGE_CLEANING
            profitTable.append([iters, currentIncome, currentExpense, currentProfit, recievedGrain, cleanedGrain, round(goodGrain, 1), round(badGrain, 1)])
            elevatorCanvas.after(INTERVAL,progress)

        totalIncome += currentIncome
        totalExpense += currentExpense
        totalProfit += currentProfit



        if (iters == kek[(len(kek)) - 1][0]):
            kek[(len(kek)) - 1] = [iters,totalProfit]
        else:
            kek.append([iters,totalProfit])

            if len(kek) > 15:               #максимальный размер массива
                del kek[0]
            if len(profitTable) > 10:       #максимальный размер таблицы
                del profitTable[0]
            drawGraph(kek)
            drawTable(profitTable)

        totalIncomeText.config(text = 'Total Income = ' + str(totalIncome) + '$')
        totalExpenceText.config(text = 'Total Expense = ' + str(totalExpense) + '$')
        totalProfitText.config(text = 'Total Profit = ' + str(totalProfit) + '$')

        print(totalIncome)
        print(totalExpense)
        print(totalProfit)

        timeGoodExportText.config(text = "Через {0} дн.".format(str(abs(iters % DISPATCH_DELAY % (-1*DISPATCH_DELAY)))))
        print()
##################################################################################

canGraph = Canvas(window, width = 780, height = 600)
canGraph.place(x = 800, y = 305)
canvasGraph = FigureCanvasTkAgg(fig, canGraph)
canvasGraph.get_tk_widget().config(bg = 'snow')
canvasGraph.get_tk_widget().grid(column=0,row=0)

canTable = Canvas(window, width = 300, height = 600)
canTable.place(x = 0, y = 305)
canvasTable = FigureCanvasTkAgg(tableFig, canTable)
canvasTable.get_tk_widget().config(bg = 'snow')
canvasTable.get_tk_widget().grid(column=0, row=0, sticky='nsew')

elevatorCanvas.after(0,progress)
window.geometry('1480x720')
window.mainloop()

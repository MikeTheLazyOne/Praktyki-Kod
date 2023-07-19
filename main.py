import os, sys, random, can
from PyQt5.QtCore import QThread, Qt, QTimer, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QHBoxLayout, QMenu, QMenuBar,\
    QLabel, QLineEdit, QFormLayout, QComboBox, QListWidget, QGridLayout
import time
import sys
import numpy as np

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pyqtgraph.exporters

debug = 0

class Worker(QObject):
    RecvMessage = Signal(list)
   

    def __init__(self, szef):
        super().__init__()
        self.szef = szef

    @Slot(int)
    def Talking(self,v):
        print("QThreads start operating")
        tablica = np.linspace(-np.pi, np.pi, 161)
        tablica = np.sin(tablica)*2
        lista = list(round(elem,2) for elem in tablica)
        lista = podziel_liste(lista, 4)
        len_of_list = len(lista)
        counter = 0
        while (v == 1):
            time.sleep(0.2)
            self.RecvMessage.emit(lista[counter])
            counter += 1
            if counter == 40:
                counter = 0               

class RightBar(QWidget):

    def __init__(self, usecase, figure, data_line):
        super().__init__()
        self.figure = figure
        self.usecase = usecase
        self.data_line = data_line
        
        self.button = QPushButton("Refressh")
        self.plot_reset_button = QPushButton("Plot Resset")
        self.cursor_line = QPushButton("Add Currssor")
        self.remove_cursor = QPushButton("Remove Currssor")
        self.trigger_button = QPushButton("AddTrigger")
        
        self.drop_down_add_cursor = QComboBox()
        self.drop_down_add_cursor.addItem("---Choose currssor to add---")
        self.drop_down_add_cursor.addItem("Add Vertical Currssor")
        self.drop_down_add_cursor.addItem("Add Horizontal Currssor")
        
        self.drop_down_add_cursor.currentIndexChanged.connect(self._dropIndexChaged)
        self.CursorPen = pg.mkPen(color = (255,0,255),width = 2, style=Qt.DashLine)
        self.TriggerPen = pg.mkPen(color = (255,0,0),width = 2, style=Qt.DotLine)
        self.lineA = pg.InfiniteLine(pos = (80,0), pen = self.CursorPen, movable = True, label= "A-cursor")
        self.lineB = pg.InfiniteLine(pos = (80,0), pen = self.CursorPen, movable = True, label= "B-cursor")
        self.lineC = pg.InfiniteLine(angle = 0, pos = (0,0), pen = self.CursorPen, movable = True, label= "C-cursor")
        self.lineD = pg.InfiniteLine(angle = 0, pos = (0,0), pen = self.CursorPen, movable = True, label= "D-cursor")
        self.trigger = pg.InfiniteLine(angle=0, pos = (0,0), pen = self.TriggerPen, movable = True, label="Trigger")
        self.list_of_Hor_cursors = list()
        self.list_of_Ver_cursors = list()
        self.list_of_Hor_cursors.append(self.lineA)
        self.list_of_Hor_cursors.append(self.lineB)
        self.list_of_Ver_cursors.append(self.lineC)
        self.list_of_Ver_cursors.append(self.lineD)
                                                                  
        self._buttonoption()
        self.status = self.button.isChecked()

        self.average = QLabel("Average")
        self.median = QLabel("Median")
        self.max = QLabel("Max")
        self.min = QLabel("Min")
        self.AxPos = QLabel("A x pos:")
        self.BxPos = QLabel("B x pos:")
        self.AyPos = QLabel("A y pos:")
        self.ByPos = QLabel("B y pos:")
        self.MaxAB = QLabel("Max AB value:")
        self.MinAB = QLabel("Min AB value:")
        self.Trigger_val = QLabel("Triger Value:")

        self.CyPos = QLabel("C y value:")
        self.DyPos = QLabel("D y value:")
        self.CxPos_one = QLabel("C x pos 1st:")
        self.CxPos_two = QLabel("C x pos 2nd:")
        self.DxPos_one = QLabel("D x pos 1st:")
        self.DxPos_two = QLabel("D x pos 2nd:")
        self.Len_CD = QLabel("Length C-D:")
        self.Len_DC = QLabel("Length D-C:")

        self.average_input = QLineEdit()
        self.median_input = QLineEdit()
        self.min_input = QLineEdit()
        self.max_input = QLineEdit()
        self.AxPos_input = QLineEdit()
        self.BxPos_input = QLineEdit()
        self.AyPos_input = QLineEdit()
        self.ByPos_input = QLineEdit()
        self.MaxAB_input = QLineEdit()
        self.MinAB_input = QLineEdit()

        self.CyPos_input = QLineEdit()
        self.DyPos_input = QLineEdit()
        self.CxPos_one_input = QLineEdit()
        self.CxPos_two_input = QLineEdit()
        self.DxPos_one_input = QLineEdit()
        self.DxPos_two_input = QLineEdit()
        self.Len_CD_input = QLineEdit()
        self.Len_DC_input = QLineEdit()

        self.Trigger_val_input = QLineEdit()
        self.trigger_active = 0
        self.trigger_start = QPushButton("Start Trigger")
        self.trigger_stop = QPushButton("Stop Trigger")


        self._labeloption()
       
        self.timer = QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start()

        self._layoutoption()
        self.counter_vertical_cursor = 0
        self.counter_horizontal_cursor = 0

        self.DataCursorVerticalLayout = QFormLayout()
        self.DataCursorVerticalLayout.setSpacing(10)
        self.DataCursorVerticalWidget = QWidget()

        self.DataCursorHorizontalLayout = QFormLayout()
        self.DataCursorHorizontalWidget = QWidget()
        # self.DataCursorWidget.setFixedHeight(1000)
        self.DataCursorHorizontalWidget.setLayout(self.DataCursorHorizontalLayout)
        self.DataCursorVerticalWidget.setLayout(self.DataCursorVerticalLayout)
        self.CursorLayout.addWidget(self.DataCursorVerticalWidget, 0, 0)
        self.CursorLayout.addWidget(self.DataCursorHorizontalWidget, 0, 1)


    def __action_to_remove_currsor(self, cur_type):
        if cur_type == 'vertical':
            self.counter_vertical_cursor -= 1
            self.figure.removeItem(self.list_of_Hor_cursors[self.counter_vertical_cursor])
            self.drop_down_add_cursor.setItemText(self.drop_down_add_cursor.currentIndex(),\
                                                    f"Add Vertical cursor ({self.counter_vertical_cursor}/2)")
        elif cur_type == 'horizontal':
            self.counter_horizontal_cursor -= 1
            self.figure.removeItem(self.list_of_Ver_cursors[self.counter_horizontal_cursor])
            self.drop_down_add_cursor.setItemText(self.drop_down_add_cursor.currentIndex(),\
                                                    f"Add horizontal cursor ({self.counter_horizontal_cursor}/2)")
        else:
            print(f"Pease specify type{cur_type}")
        
    def __action_to_add_currsor(self, cur_type):
        if cur_type == 'vertical':
            self.counter_vertical_cursor += 1
            self.drop_down_add_cursor.setItemText(self.drop_down_add_cursor.currentIndex(),\
                                                        f"Add Vertical cursor ({self.counter_vertical_cursor}/2)")

            self.figure.addItem(self.list_of_Hor_cursors[self.counter_vertical_cursor-1])
        elif cur_type == 'horizontal':
            self.counter_horizontal_cursor += 1
            self.drop_down_add_cursor.setItemText(self.drop_down_add_cursor.currentIndex(),\
                                                    f"Add horizontal cursor ({self.counter_horizontal_cursor}/2)")
            self.figure.addItem(self.list_of_Ver_cursors[self.counter_horizontal_cursor-1])
        else:
            print("fplease specify type:{cur_type}")

    def _remove_buttin_action(self):
        if self.drop_down_add_cursor.currentIndex() == 0:
            print("please choose correct cursor")
            self.drop_down_add_cursor.setItemText(self.drop_down_add_cursor.currentIndex(),\
                                                   f"please choose correct cursor")
        elif self.drop_down_add_cursor.currentIndex() == 1:
            
            if self.counter_vertical_cursor <= 2 and self.counter_vertical_cursor != 0:
                self.__action_to_remove_currsor('vertical')
                
                if self.counter_vertical_cursor ==1:
                    self.__takeRowargs(self.DataCursorVerticalLayout, self.BxPos, self.ByPos, self.MaxAB, self.MinAB)
                elif self.counter_vertical_cursor == 0:
                    self.__takeRowargs(self.DataCursorVerticalLayout, self.AyPos, self.AxPos)
            elif self.drop_down_add_cursor.currentIndex() == 0:
                self.drop_down_add_cursor.setItemText(self.drop_down_add_cursor.currentIndex(),\
                                                    f"Add Vertical cursor ({self.counter_vertical_cursor}/2)")

        elif self.drop_down_add_cursor.currentIndex() == 2:
            
            if self.counter_horizontal_cursor <= 2 and self.counter_horizontal_cursor != 0:
                self.__action_to_remove_currsor('horizontal')
                if self.counter_horizontal_cursor ==1:
                    self.__takeRowargs(self.DataCursorHorizontalLayout, self.CyPos, self.CxPos_one, self.CxPos_two)
                elif self.counter_horizontal_cursor == 0:
                    self.__takeRowargs(self.DataCursorHorizontalLayout, self.DyPos, \
                                       self.DxPos_one, self.DxPos_two, self.Len_CD, self.Len_DC)
                    
            elif self.drop_down_add_cursor.currentIndex() == 0:
                self.drop_down_add_cursor.setItemText(self.drop_down_add_cursor.currentIndex(),\
                                                    f"Add horizontal cursor ({self.counter_horizontal_cursor}/2)")

    def __takeRowargs(self, z, *args):
        for i in range(len(args)):
            z.takeRow(args[i])

    def __addRowArgs(self, z, *args):
        for i in range(len(args)):
            if type(args[i]) == tuple:
                z.addRow(args[i][0], args[i][1])
            else:
                z.addRow(args[i])

    def _add_button_action(self):
        if self.drop_down_add_cursor.currentIndex() == 0:
            print("please choose correct cursor")
            self.drop_down_add_cursor.showPopup()
            self.drop_down_add_cursor.setItemText(self.drop_down_add_cursor.currentIndex(),\
                                                   f"Please choose correct cursor")
            
        elif self.drop_down_add_cursor.currentIndex() == 1:
            
            if self.counter_vertical_cursor != 2:
                self.__action_to_add_currsor('vertical')
                if self.counter_vertical_cursor == 1:
                    self.__addRowArgs(self.DataCursorVerticalLayout, (self.AxPos, self.AxPos_input), (self.AyPos, self.AyPos_input))
                if self.counter_vertical_cursor == 2:
                    self.__addRowArgs(self.DataCursorVerticalLayout, (self.BxPos, self.BxPos_input), (self.ByPos, self.ByPos_input),\
                                    (self.MaxAB, self.MaxAB_input), (self.MinAB, self.MinAB_input) )
            else:
                self.drop_down_add_cursor.setItemText(self.drop_down_add_cursor.currentIndex(),\
                                                    f"Limit achived!")
        elif self.drop_down_add_cursor.currentIndex() == 2:
            
            if self.counter_horizontal_cursor != 2:
                self.__action_to_add_currsor('horizontal')
                if self.counter_horizontal_cursor == 1:
                    self.__addRowArgs(self.DataCursorHorizontalLayout, (self.CyPos, self.CyPos_input),\
                                       (self.CxPos_one, self.CxPos_one_input), (self.CxPos_two, self.CxPos_two_input))
                    
                if self.counter_horizontal_cursor == 2:
                    self.__addRowArgs(self.DataCursorHorizontalLayout, (self.DyPos, self.DyPos_input), (self.DxPos_one, self.DxPos_one_input),\
                                      (self.DxPos_two, self.DxPos_two_input), (self.Len_CD, self.Len_CD_input), (self.Len_DC, self.Len_DC_input))
            else:
                self.drop_down_add_cursor.setItemText(self.drop_down_add_cursor.currentIndex(),\
                                                    f"Limit achived!")
       
    def _dropIndexChaged(self, index):
        print("Activated index:", index)

    def _labeloption(self):
       
        self.average.setAlignment(Qt.AlignRight)
        self.median.setAlignment(Qt.AlignRight)
        self.max.setAlignment(Qt.AlignRight)
        self.min.setAlignment(Qt.AlignRight)

        self.average.setMinimumSize(150, 30)
        self.median.setMinimumSize(150, 30)
        self.max.setMinimumSize(150, 30)
        self.min.setMinimumSize(150, 30)

    def _buttonwork(self):
        self.status = self.button.isChecked()
        print(f"Refresh status chaged to {self.status}")

    def get_button_status(self):
        return self.status

    def _buttonoption(self):
        self.button.clicked.connect(lambda: self._buttonwork())
        self.plot_reset_button.clicked.connect(lambda: self.usecase.plot.getPlotItem().enableAutoRange())
        
        self.cursor_line.clicked.connect(self._add_button_action)
        self.remove_cursor.clicked.connect(self._remove_buttin_action)
        self.trigger_button.clicked.connect(self.__add_triger)
        self.button.setCheckable(True)
        self.button.setChecked(True)
        self.button.setMinimumSize(300, 30)
        self.plot_reset_button.setMinimumSize(300, 30)

    def __add_triger(self):
        self.trigger_active = 1
        print("trigger added")
        self.figure.addItem(self.trigger)

    def _layoutoption(self):

        self.layout = QFormLayout()
        # adding widgets
        self.__addRowArgs(self.layout, self.button, self.plot_reset_button,(self.average, self.average_input), \
                          (self.median, self.median_input), (self.max, self.max_input),\
                         (self.min, self.min_input), self.drop_down_add_cursor, self.cursor_line, self.remove_cursor)
        
        self.setFixedWidth(400)
        self.setLayout(self.layout)
        self.CursorWidget = QWidget()
        self.CursorLayout = QGridLayout()
        
        self.CursorWidget.setLayout(self.CursorLayout)
        self.__addRowArgs(self.layout, self.CursorWidget, self.trigger_button, (self.Trigger_val, self.Trigger_val_input))

    def update_labels(self):
        if self.trigger_active == 1:
            self.Trigger_val_input.setText(f"{round(self.trigger.getYPos(), 2)}")
            value = self.data_line.getData()[1][-1]
            value_prev = self.data_line.getData()[1][-6]
            if value >= round(self.trigger.getYPos(), 2) and round(self.trigger.getYPos(), 2) >= value_prev:
                self.status = self.button.setChecked(False)
                print("jest góra")
            if value <= round(self.trigger.getYPos(), 2) and round(self.trigger.getYPos(), 2) <= value_prev:
                self.status = self.button.setChecked(False)
                print("jest dół")
       
        if self.get_button_status() == True:
            self.average_input.setText(f"{round(np.average(self.usecase.get_ydata()), 2)}")
            self.median_input.setText(f"{round(np.median(self.usecase.get_ydata()), 2)}")
            self.max_input.setText(f"{round(np.max(self.usecase.get_ydata()), 2)}")
            self.min_input.setText(f"{round(np.min(self.usecase.get_ydata()), 2)}")
           
        else:
            if debug == 1:
                print("Refresh is off")
        if self.counter_vertical_cursor != 0:
            AxPos = self.lineA.getXPos()
            self.AxPos_input.setText(f"{int(AxPos)}")
            self.AyPos_input.setText(f"{self.data_line.getData()[1][int(AxPos)]}")
            if self.counter_vertical_cursor == 2:
                BxPos = self.lineB.getXPos()
                self.BxPos_input.setText(f"{int(self.lineB.getXPos())}")
                self.ByPos_input.setText(f"{self.data_line.getData()[1][int(BxPos)]}")
                if AxPos < BxPos:
                    MaxAB = self.data_line.getData()[1][int(AxPos):int(BxPos)]
                    self.MaxAB_input.setText(f"{np.max(MaxAB)}")
                    self.MinAB_input.setText(f"{np.min(MaxAB)}")
                elif BxPos < AxPos:
                    MaxAB = self.data_line.getData()[1][int(BxPos):int(AxPos)]
                    self.MaxAB_input.setText(f"{np.max(MaxAB)}")
                    self.MinAB_input.setText(f"{np.min(MaxAB)}")
                else:
                    MaxAB = None
                    self.MaxAB_input.setText(f"None")
                    self.MinAB_input.setText(f"None")
        if self.counter_horizontal_cursor != 0:
            
            CyPos = self.lineC.getYPos()
            self.CyPos_input.setText(f"{round(CyPos, 2)}")
            lista = self.data_line.getData()[1]
            self.CxPos_one_input.setText(f"{closest_value(lista, CyPos)}")
            

class MainWindow(QMainWindow):
    talking = Signal(int)
    def __init__(self):
        super().__init__()
        
        self.set_ndata()
        self.ydata = [0 for i in range(self.n_data)]
        self._view()
        # its have to be here to give it abbility to have cusors and triggers
        self.plot = pg.PlotWidget()
        self.pen = pg.mkPen(color= (0,255,0), width = 3)
        self.data_line =  pg.PlotCurveItem(self.xdata, self.ydata, pen=self.pen)
        # RightBar is a class to show information like median or average also later can be used for sending data
        self.menu_bar = RightBar(self, self.plot, self.data_line)
        # test of reset button
        
        self._plotSetUp()
        # self.test_btn = QPushButton("reset")
        # self.test_btn.clicked.connect(lambda: self.plot.getPlotItem().enableAutoRange())
        self._threadSetUp()
        
        self._timerSetUp()
                
        self._layoutoption()

        # Setting Widget for layout to show in center still don't know to make toolbar
        widget = QWidget()
        widget.setLayout(self.main_window_layout)
        self.setCentralWidget(widget)
        # creating menu bar at top of the app
        self._menumake()
        self.id = 0
        self.showMaximized()
    
    def notify(self, receiver, event):
        try:
            return super().notify(receiver, event)
        except Exception as e:
            print("Exception caught:", e)
            # Dodaj tutaj kod obsługi wyjątku
            # np. wyświetlanie komunikatu o błędzie, zamykanie aplikacji itp.
            return False
    def savePlotToFile(self):
        
        pngexporter = pyqtgraph.exporters.ImageExporter(self.plot.plotItem)
        csvexporter = pyqtgraph.exporters.CSVExporter(self.plot.plotItem)
        pngexporter.parameters()['width'] = 600
        pngexporter.export(f'Plot-{self.id}.png')
        csvexporter.export(f"Data for plot-{self.id}.csv")
        print(f"file saved with id = {self.id}")
        self.id += 1

    def _threadSetUp(self):
        # Worker
        self.worker = Worker(self)
        # Thread
        self.worker_thread = QThread()
        self.worker.RecvMessage.connect(self.set_addData)
        self.talking.connect(self.worker.Talking)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        self.talking.emit(1)   

    def _plotSetUp(self):
        
        self.plot.setBackground('w')
        
        self.plot.addItem(self.data_line)    
        self.plot.setXRange(0,160)

    def _timerSetUp(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def _view(self):
        self.setWindowTitle("My App")
        self.setMinimumSize(400, 500)

    def _layoutoption(self):
        self.main_window_layout = QHBoxLayout()
        # adding Widgets to layout
        
        self.main_window_layout.addWidget(self.plot)
        self.main_window_layout.addWidget(self.menu_bar)
        self.main_window_layout.setAlignment(Qt.AlignCenter)

    def _menumake(self):
        # Menu bar and options
        menubar = QMenuBar(self)

        # creating some toolbars for file and other things
        filemenu = QMenu("&File", self)
        filemenu.addAction("Save", lambda : self.savePlotToFile())
        filemenu.addAction("Errors", lambda : print("There are no Errors program runs fine"))

        helpmenu = QMenu("&Help", self)
        helpmenu.addAction("Help", lambda: print("there is no help :D"))
        menubar.addMenu(filemenu)
        menubar.addMenu(helpmenu)
        self.setMenuBar(menubar)

    def _buttonwork(self):

        print("button clicked!\nand it hurts!")

    def update_plot(self):
       
        tok = time.time()
       
        if debug == 1:
            print(type(self.addData))
        
        if self.menu_bar.get_button_status() == True:
            self.data_line.setData(self.xdata, self.ydata)

        if debug == 1:
            print(self.ydata)
        
        else:
            if debug == 1:
                print("Refresh is off")

        tik = time.time()
        if (tik-tok) > 0.01:
            print(f"Failure to be fast enough: {tik-tok}")
        
       
    def get_ydata(self):
        return self.ydata
    def set_addData(self, value = 0):
        if type(value) == list:
            for data in value:
                self.ydata.pop(0)
                self.ydata.append(data)
        else:
            self.addData = list()
            self.addData.append(value)
            self.ydata = self.ydata[1:] + self.addData

    def set_ndata(self, value = 160):
        self.n_data = value
        self.xdata = list(range(self.n_data))

       
def Average(data):
    value = 0
    if data != None:
        for i in data:
            value += i
    else:
        print("data is None")
    return (value/len(data))

def isNegative(x):
    if x[0] == '-':
        return True
    else:
        return False
   
def isSmall(x):
    if type(x)==str:
        if x[0] == '0':
            return True
        else:
            return False
    elif type(x)== float:
        if x < 0.1:
            return True
        else:
            return False
       
def logic(x, y):
    if len(y) == 1:
        y = y + '0'
    if (isNegative(x) == True and isSmall(y) == False):
        y = '1' + y
    elif (isNegative(x) == True and isSmall(y) == True):
        Imp = y[-1]
        y = '21' + Imp
    elif (isNegative(x) == False and isSmall(y) == True):
        y = '2' + y  
    else:
        y = y
    return x, y

def coding(x):
    x = x.round(2)
   
    whole, dec = str(x).split(".")
    whole, dec = logic(whole, dec)
    whole = int(whole)
    dec = int(dec)
   
    if whole < 0:
        whole = whole*(-1)
   
    return (whole, dec)

def float_maker(x, y):
    x = str(x)
    y = str(y)
    num = (x+"."+y)
   
    return float(num)

def decoding(x, y):
    num = float()
    if type(x) != int:
        x = int(x, 2)

    if type(y) != int:
        y = int(y, 2)
   
    if (y >= 0 and y < 100):
        num = float_maker(x, y)
        return num
    elif (y >= 100 and y < 200):
       
        y = y - 100
        num = float_maker(x, y)
        return (num*(-1))
    elif (y >= 200 and y < 210):
       
        y = y - 200
        x = str(x)
        y = str(y)
        num = (x+".0"+y)
        num = float(num)
        return num
    elif (y>= 210 and y < 220):
       
        y = y - 210
        x = str(x)
        y = str(y)
        num = (x+".0"+y)
        num = float(num)
        return (num*(-1))
    #print(f"decoding: x = {x}, y = {y}")
    print("You are in ShitHole")

def podziel_liste(lista, rozmiar):
    return[lista[i:i+rozmiar] for i in range(0,len(lista), rozmiar)]

def closest_value(lista, value):
    return min (lista, key= lambda x: abs(x-value))


if __name__ == '__main__':

    app = QApplication(sys.argv)

    Mwindow = MainWindow()
    Mwindow.show()
    status = app.exec()

    print(f"Program Finished with status: {status}")

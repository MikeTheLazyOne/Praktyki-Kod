import os, sys, random, can
from PyQt5.QtCore import QThread, Qt, QTimer, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QHBoxLayout, QMenu, QMenuBar,\
    QLabel, QLineEdit, QFormLayout, QComboBox, QListWidget
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
        
        self.button = QPushButton("Refresh")
        self.plot_reset_button = QPushButton("Plot Reset")
        self.cursor_line = QPushButton("Add Cursor")
        self.remove_cursor = QPushButton("Remove Curssor")
        
        self.drop_down_add_curssor = QComboBox()
        self.drop_down_add_curssor.addItem("---Choose curssor to add---")
        self.drop_down_add_curssor.addItem("Add Vertical Curssor")
        self.drop_down_add_curssor.addItem("Add Horizontal Curssor")
        
        self.drop_down_add_curssor.currentIndexChanged.connect(self._dropIndexChaged)
        self.CursorPen = pg.mkPen(color = (255,0,255),width = 2, style=Qt.DashLine)
        self.lineA = pg.InfiniteLine(pos = (80,0), pen = self.CursorPen, movable = True, label= "A-curssor")
        
        
        self.lineB = pg.InfiniteLine(pos = (80,0), pen = self.CursorPen, movable = True, label= "B-curssor")
        self.lineC = pg.InfiniteLine(angle = 0,pos = (0,0), pen = self.CursorPen, movable = True, label= "C-curssor")
        self.lineD = pg.InfiniteLine(angle = 0,pos = (0,0), pen = self.CursorPen, movable = True, label= "D-curssor")
        self.list_of_Hor_curssors = list()
        self.list_of_Ver_curssors = list()
        self.list_of_Hor_curssors.append(self.lineA)
        self.list_of_Hor_curssors.append(self.lineB)
        self.list_of_Ver_curssors.append(self.lineC)
        self.list_of_Ver_curssors.append(self.lineD)
        
                                                                   
        self._buttonoption()
        self.status = self.button.isChecked()

        self.average = QLabel("average")
        self.median = QLabel("median")
        self.max = QLabel("Max")
        self.min = QLabel("Min")

        self.average_input = QLineEdit()
        self.median_input = QLineEdit()
        self.min_input = QLineEdit()
        self.max_input = QLineEdit()

        self._labeloption()
       

        self.timer = QTimer()
        self.timer.setInterval(400)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start()

        self._layoutoption()
        self.counter_vertical_cursor = 0
        self.counter_horizontal_cursor = 0
        
        
        

    def _remove_buttin_action(self):
        if self.drop_down_add_curssor.currentIndex() == 0:
            print("please choose correct curssor")
            self.drop_down_add_curssor.setItemText(self.drop_down_add_curssor.currentIndex(),\
                                                   f"please choose correct curssor")
        elif self.drop_down_add_curssor.currentIndex() == 1:
            
            if self.counter_vertical_cursor <= 2 and self.counter_vertical_cursor != 0:
                self.counter_vertical_cursor -= 1
                self.figure.removeItem(self.list_of_Hor_curssors[self.counter_vertical_cursor-1])
                self.drop_down_add_curssor.setItemText(self.drop_down_add_curssor.currentIndex(),\
                                                    f"Add Vertical curssor ({self.counter_vertical_cursor}/2)")
                
            elif self.drop_down_add_curssor.currentIndex() == 0:
                self.drop_down_add_curssor.setItemText(self.drop_down_add_curssor.currentIndex(),\
                                                    f"Add Vertical curssor ({self.counter_vertical_cursor}/2)")

        elif self.drop_down_add_curssor.currentIndex() == 2:
            
            if self.counter_horizontal_cursor <= 2 and self.counter_horizontal_cursor != 0:
                self.counter_horizontal_cursor -= 1
                self.figure.removeItem(self.list_of_Ver_curssors[self.counter_horizontal_cursor-1])
                self.drop_down_add_curssor.setItemText(self.drop_down_add_curssor.currentIndex(),\
                                                    f"Add horizontal curssor ({self.counter_horizontal_cursor}/2)")
            elif self.drop_down_add_curssor.currentIndex() == 0:
                self.drop_down_add_curssor.setItemText(self.drop_down_add_curssor.currentIndex(),\
                                                    f"Add horizontal curssor ({self.counter_horizontal_cursor}/2)")

    def _Add_button_action(self):
        if self.drop_down_add_curssor.currentIndex() == 0:
            print("please choose correct curssor")
            self.drop_down_add_curssor.setItemText(self.drop_down_add_curssor.currentIndex(),\
                                                   f"please choose correct curssor")
        elif self.drop_down_add_curssor.currentIndex() == 1:
            
            if self.counter_vertical_cursor != 2:
                self.counter_vertical_cursor += 1
                self.drop_down_add_curssor.setItemText(self.drop_down_add_curssor.currentIndex(),\
                                                    f"Add Vertical curssor ({self.counter_vertical_cursor}/2)")
                # if self.counter_vertical_cursor == 1:
                #     self.figure.addItem(self.list_of_Hor_curssors[0])
                # elif self.counter_vertical_cursor == 2:
                #     self.figure.addItem(self.list_of_Hor_curssors[1])
                self.figure.addItem(self.list_of_Hor_curssors[self.counter_vertical_cursor-1])
                
            else:
                self.drop_down_add_curssor.setItemText(self.drop_down_add_curssor.currentIndex(),\
                                                    f"Limit achived!")
        elif self.drop_down_add_curssor.currentIndex() == 2:
            
            if self.counter_horizontal_cursor != 2:
                self.counter_horizontal_cursor += 1
                self.drop_down_add_curssor.setItemText(self.drop_down_add_curssor.currentIndex(),\
                                                    f"Add horizontal curssor ({self.counter_horizontal_cursor}/2)")
                self.figure.addItem(self.list_of_Ver_curssors[self.counter_horizontal_cursor-1])
            else:
                self.drop_down_add_curssor.setItemText(self.drop_down_add_curssor.currentIndex(),\
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
        # lambda : self.usecase.plot.removeItem(self.usecase.line)
        self.cursor_line.clicked.connect(self._Add_button_action)
        self.remove_cursor.clicked.connect(self._remove_buttin_action)
        self.button.setCheckable(True)
        self.button.setChecked(True)
        self.button.setMinimumSize(300, 30)
        self.plot_reset_button.setMinimumSize(300, 30)
        #self.button.setAligment(Qt.AlignRight)

    def _layoutoption(self):

        self.layout = QFormLayout()
        # adding widgets
        self.layout.addRow(self.button)
        self.layout.addRow(self.plot_reset_button)
        self.layout.addRow(self.average, self.average_input)
        self.layout.addRow(self.median, self.median_input)
        self.layout.addRow(self.max, self.max_input)
        self.layout.addRow(self.min, self.min_input)
        self.layout.addRow(self.drop_down_add_curssor)
        self.layout.addRow(self.cursor_line)
        self.layout.addRow(self.remove_cursor)
        self.setFixedSize(350, 600)
        self.setLayout(self.layout)
    
    def update_labels(self):
       
        if self.get_button_status() == True:
            self.average_input.setText(f"{round(np.average(self.usecase.get_ydata()), 2)}")
            self.median_input.setText(f"{round(np.median(self.usecase.get_ydata()), 2)}")
            self.max_input.setText(f"{round(np.max(self.usecase.get_ydata()), 2)}")
            self.min_input.setText(f"{round(np.min(self.usecase.get_ydata()), 2)}")
           
        else:
            if debug == 1:
                print("Refresh is off")
    
class MainWindow(QMainWindow):
    talking = Signal(int)
    def __init__(self):
        super().__init__()

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
        # self.plot = pg.PlotWidget()
        # self.pen = pg.mkPen(color= (0,255,0), width = 3)
        # self.data_line =  pg.PlotCurveItem(self.xdata, self.ydata, pen=self.pen)
        # self.CursorPen = pg.mkPen(color = (255,0,0),width = 2, style=Qt.DashLine)
        self.plot.setBackground('w')
        self.set_ndata()
        self.ydata = [0 for i in range(self.n_data)]
        # self.line = pg.InfiniteLine(pos = (80,0), pen = self.CursorPen, movable = True)
        # self.plot.addItem(self.line)
        self.Cursor_pos = int()
        self.Cross_point = int()
        
        
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
        # Cursor working good but i have to add some options but i will have to give i Right_bar
        # self.Cursor_pos = int(self.line.getPos()[0])
        # self.Cross_point = self.data_line.getData()[1][self.Cursor_pos]
        # print(f"line x posttion  = {self.Cursor_pos}")
        # print(f"line x Value  = {self.Cross_point}")
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


if __name__ == '__main__':

    app = QApplication(sys.argv)

    Mwindow = MainWindow()
    Mwindow.show()
    status = app.exec()

    print(f"Program Finished with status: {status}")

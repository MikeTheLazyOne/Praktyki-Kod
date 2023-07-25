import os, sys, random, can
import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, Qt, QTimer, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QHBoxLayout, QMenu, QMenuBar,\
    QLabel, QLineEdit, QFormLayout, QComboBox, QListWidget, QGridLayout, QCheckBox, QStyle
import time
import sys
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pyqtgraph.exporters
import PyQt5
debug = 0

class Worker(QObject):
    RecvMessage = Signal(dict)
   

    def __init__(self, szef):
        super().__init__()
        self.szef = szef

    @Slot(int)
    def Talking(self,v):
        print("QThreads start operating")
        
        tablica = np.linspace(-np.pi, np.pi, 161)
        tablica = np.sin(tablica)*2
        cos = np.cos(tablica)
        lista = list(round(elem,2) for elem in tablica)
        lista = podziel_liste(lista, 4)
        
        lista_2 = list(round(elem,2) for elem in cos)
        lista_2 = podziel_liste(lista_2, 4)
        counter = 0
        while (v == 1):
            time.sleep(0.2)
            data = {123:lista[counter]}
            data_2 = {321:lista_2[counter]}
            self.RecvMessage.emit(data)
            self.RecvMessage.emit(data_2)
            counter += 1
            if counter == 40:
                counter = 0
class Postman(QObject):
    Yepper = Signal(str)
    def __init__(self):
        super().__init__()
        
    @Slot(dict)
    def Running(self, message):
        print("HE is talking")
        # os.system('sudo ip link set can0 type can bitrate 100000')
        # os.system('sudo ifconfig can0 up')

        # can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native

        # for id, data in message.items():
        #     id = hex(id)
        #     data = bytearray(data)
        #     msg = can.Message(arbitration_id=id, data= data, is_extended_id=False)
        #     can0.send(msg)
        # os.system('sudo ifconfig can0 down')
class Trigger_buttons(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.start = QPushButton()
        self.stop = QPushButton()
        
       
        
        self.start.setIcon(QIcon('ok_2.png'))
        self.stop.setIcon(QIcon('stop_3.png'))
        
        
        self.start.setIconSize(QSize(50,50))
        self.stop.setIconSize(QSize(50,50))
        

        self.start.setFixedHeight(75)
        self.start.setFixedWidth(75)
        self.stop.setFixedHeight(75)
        self.stop.setFixedWidth(75)
        

        self.start.setCheckable(True)
        self.stop.setCheckable(True)
        self.start.isChecked()

        self.start.clicked.connect(self.start_action)
        self.stop.clicked.connect(self.stop_action)
        

        self.addWidget(self.start)
        self.addWidget(self.stop)
        
    
    def start_action(self):
        self.status_start = self.start.isChecked()
        if self.status_stop == True:
            self.stop.click()
    def stop_action(self):
        self.status_stop = self.stop.isChecked()
        if self.status_start == True:
            self.start.click()
    
    def get_start(self):
        return self.status_start
    def get_stop(self):
        return self.status_stop
    
class SendWindow(QWidget):
    talking = Signal(dict)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Send Message")
        self.layout = QHBoxLayout()
        self.id = QLabel("ID: ")
        self.id_input  = QLineEdit()
        self.message = QLabel("Message: ")
        self.message_input = QLineEdit()
        self.send  = QPushButton("Send")
        self.send.clicked.connect(self.send_action)

        self.layout.addWidget(self.id)
        self.layout.addWidget(self.id_input)
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.message_input)
        self.layout.addWidget(self.send)

        self.worker = Postman()  # Worker
        self.worker_thread = QThread()  # Thread
        self._threadSetUp()
        
        self.setLayout(self.layout)

    def send_action(self):
        # Wokrker thread taking message and sending it somewhere
        data = {int(self.id_input.text()):int(self.message_input.text())}
        print(f"Message with {self.id_input.text()} was send with data: {self.message_input.text()}")
        print(data)
        self.talking.emit(data)
        self.close()
    def _threadSetUp(self):
        
        self.worker.Yepper.connect(self.confirmation)
        self.talking.connect(self.worker.Running)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        
    def confirmation(self, text):
        print(text)
class AnotherWindow(QWidget):
    def __init__(self, title, usecase):
        super().__init__()
        self.usecase = usecase
        self.setWindowTitle(title)
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        self.ok_button = QPushButton("Apply")
        self.widget_1 = QWidget()
        self.widget_2 = QWidget()
        self.widget_3 = QWidget()
        self.widget_4 = QWidget()
        self.widget_5 = QWidget()
        self.plotlayouts = list()
        self.plotlayouts.append(PlotOptions(1, True, "sinus", "123"))
        self.plotlayouts.append(PlotOptions(2))
        self.plotlayouts.append(PlotOptions(3))
        self.plotlayouts.append(PlotOptions(4))
        self.plotlayouts.append(PlotOptions(5))
        self.widget_1.setLayout(self.plotlayouts[0]) 
        self.widget_2.setLayout(self.plotlayouts[1])
        self.widget_3.setLayout(self.plotlayouts[2])
        self.widget_4.setLayout(self.plotlayouts[3])
        self.widget_5.setLayout(self.plotlayouts[4])
        layout.addWidget(self.label)
        layout.addWidget(self.widget_1)
        layout.addWidget(self.widget_2)
        layout.addWidget(self.widget_3)
        layout.addWidget(self.widget_4)
        layout.addWidget(self.widget_5)
        layout.addWidget(self.ok_button)
        self.ok_button.clicked.connect(self.ok_button_action)
        self.setLayout(layout)
        self.frameSize = 10

    def ok_button_action(self):
        self.usecase._plotSetUp()
        self.close()

class PlotOptions(QVBoxLayout):

    def __init__(self, index, status = False, name = "-- Choose name --", id = "-- Choose ID --"):
        super().__init__()
        self.index = index
        self.NewLayout = QHBoxLayout()
        self.plotname  = QLabel(f"Plot-{index} Name")
        self.plotname_input = QLineEdit(name)
        self.plotid = QLabel("Plot ID:")
        self.plotid_input = QLineEdit(id)
        self.check = QCheckBox()
        self.check.setChecked(status)
        self.NewLayout.addWidget(self.check)
        self.NewLayout.addWidget(self.plotname)
        self.NewLayout.addWidget(self.plotname_input)
        self.NewLayout.addWidget(self.plotid)
        self.NewLayout.addWidget(self.plotid_input)
        
        self.widget_one = QWidget()
        self.widget_one.setLayout(self.NewLayout)
        self.addWidget(self.widget_one)
        self.plotname_input.editingFinished.connect(self.__name_changed)
        self.plotid_input.editingFinished.connect(self.__id_changed)

    def get_index(self):
        return self.index
    
    def get_name(self):
        return self.plotname_input.text()
    
    def get_id(self):
        return self.plotid_input.text()
    
    def set_name(self, new_name):
        self.plotname_input.setText(new_name)

    def set_id(self, new_id):
        self.plotid_input.setText(new_id)

    def get_check(self):
        return self.check.isChecked()
    
    def __name_changed(self):
        #usecase -> mainWindow -> change plotname
        print(f"text changed of plot-{self.index} to: {self.plotname_input.displayText()}")
        
    def __id_changed(self):
        print(f"id of plot-{self.index} to: {self.plotid_input.displayText()}")

class RightBar(QWidget):

    def __init__(self, usecase, figure, data_line):
        super().__init__()
        self.figure = figure
        self.usecase = usecase
        self.data_line = data_line
        
        self.button = QPushButton("Refressh")
        self.button.setIcon(QIcon('go_3.png'))
        self.plot_reset_button = QPushButton("Plot Resset")
        self.plot_reset_button.setIcon(QIcon('restart.png'))
        self.cursor_line = QPushButton("Add Currssor")
        self.remove_cursor = QPushButton("Remove Currssor")
        self.trigger_button = QPushButton("AddTrigger")

        self.ButtonsHlayout = QHBoxLayout()
        self.ButtonsHlayout.addWidget(self.button)
        self.ButtonsHlayout.addWidget(self.plot_reset_button)
        self.Widget_BHL = QWidget()
        self.Widget_BHL.setLayout(self.ButtonsHlayout)

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

        self.Plot_of_intrest = QLabel("Plot of interest")
        self.Chooser = QComboBox()
        self._chooserSetup()

        self.CyPos_input = QLineEdit()
        self.DyPos_input = QLineEdit()
        self.CxPos_one_input = QLineEdit()
        self.CxPos_two_input = QLineEdit()
        self.DxPos_one_input = QLineEdit()
        self.DxPos_two_input = QLineEdit()
        self.Len_CD_input = QLineEdit()
        self.Len_DC_input = QLineEdit()

        self.Trigger_val_input = QLineEdit()
        self.trigger_active = False
        self.trigger_start = QPushButton("Start Trigger")
        self.trigger_stop = QPushButton("Stop Trigger")


        self._labeloption()
       
        self.timer = QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start()

        self.CursorWidget = QWidget()
        self.CursorLayout = QGridLayout()
        

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

        self.trigger_buttons = Trigger_buttons()
        self.Widget_for_trigger_buttons = QWidget()
        self.Widget_for_trigger_buttons.setLayout(self.trigger_buttons)
        self._layoutoption()

    def _chooserSetup(self):
        self.Chooser.addItem("1")
        self.Chooser.addItem("2")
        self.Chooser.addItem("3")
        self.Chooser.addItem("4")
        self.Chooser.addItem("5")

    def __action_to_remove_currsor(self, cur_type = None):
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
            print(f"Pease specify type {cur_type}")
        
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
                    self.__addRowArgs(self.DataCursorHorizontalLayout, (self.CyPos, self.CyPos_input))
                    
                if self.counter_horizontal_cursor == 2:
                    self.__addRowArgs(self.DataCursorHorizontalLayout, (self.DyPos, self.DyPos_input), \
                                      (self.Len_CD, self.Len_CD_input))
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

    def buttonwork(self):
        self.status = self.button.isChecked()
        print(f"Refresh status chaged to {self.status}")

    def get_button_status(self):
        return self.status

    def set_button_status(self):
        self.status = self.button.isDown()
        

    def _buttonoption(self):
        self.button.clicked.connect(lambda: self.buttonwork())
        self.plot_reset_button.clicked.connect(lambda: self.usecase.plot.getPlotItem().enableAutoRange())
        
        self.cursor_line.clicked.connect(self._add_button_action)
        self.remove_cursor.clicked.connect(self._remove_buttin_action)
        self.trigger_button.clicked.connect(self.__add_triger)
        self.button.setCheckable(True)
        # self.button.setChecked(True)
        self.button.setMinimumHeight(50)
        self.plot_reset_button.setMinimumHeight(50) 

    def __add_triger(self):
        self.trigger_active = True
        print("Trigger added")
        self.figure.addItem(self.trigger)
        self.__addRowArgs(self.layout, self.Widget_for_trigger_buttons)

    def _layoutoption(self):

        self.layout = QFormLayout()
        # adding widgets
        self.__addRowArgs(self.layout, self.Widget_BHL, (self.Plot_of_intrest, self.Chooser), (self.average, self.average_input), \
                          (self.median, self.median_input), (self.max, self.max_input),\
                         (self.min, self.min_input), self.drop_down_add_cursor, self.cursor_line, self.remove_cursor)
        
        self.setFixedWidth(400)
        self.setLayout(self.layout)
        self.CursorWidget.setLayout(self.CursorLayout)
        self.__addRowArgs(self.layout, self.CursorWidget, self.trigger_button,\
                           (self.Trigger_val, self.Trigger_val_input))

    def update_labels(self):
        if self.trigger_active == True and self.trigger_buttons.get_start() == True:
            self.Trigger_val_input.setText(f"{round(self.trigger.getYPos(), 2)}")
            value = self.data_line[self.Chooser.currentIndex()].getData()[1][20]
            value_prev = self.data_line[self.Chooser.currentIndex()].getData()[1][30]
            if value >= round(self.trigger.getYPos(), 2) and round(self.trigger.getYPos(), 2) >= value_prev:
                self.status = self.button.setChecked(False)
                print("jest góra")
            if value <= round(self.trigger.getYPos(), 2) and round(self.trigger.getYPos(), 2) <= value_prev:
                self.status = self.button.setChecked(False)
                print("jest dół")
       
        if self.get_button_status() == True:
            self.average_input.setText(f"{round(np.average(self.data_line[self.Chooser.currentIndex()].getData()[1]), 2)}")
            self.median_input.setText(f"{round(np.median(self.data_line[self.Chooser.currentIndex()].getData()[1]), 2)}")
            self.max_input.setText(f"{round(np.max(self.data_line[self.Chooser.currentIndex()].getData()[1]), 2)}")
            self.min_input.setText(f"{round(np.min(self.data_line[self.Chooser.currentIndex()].getData()[1]), 2)}")
           
        else:
            if debug == 1:
                print("Refresh is off")
        if self.counter_vertical_cursor != 0:
            AxPos = self.lineA.getXPos()
            self.AxPos_input.setText(f"{int(AxPos)}")
            self.AyPos_input.setText(f"{self.data_line[self.Chooser.currentIndex()].getData()[1][int(AxPos)]}")
            if self.counter_vertical_cursor == 2:
                BxPos = self.lineB.getXPos()
                self.BxPos_input.setText(f"{int(self.lineB.getXPos())}")
                self.ByPos_input.setText(f"{self.data_line[self.Chooser.currentIndex()].getData()[1][int(BxPos)]}")
                if AxPos < BxPos:
                    MaxAB = self.data_line[self.Chooser.currentIndex()].getData()[1][int(AxPos):int(BxPos)]
                    self.MaxAB_input.setText(f"{np.max(MaxAB)}")
                    self.MinAB_input.setText(f"{np.min(MaxAB)}")
                elif BxPos < AxPos:
                    MaxAB = self.data_line[self.Chooser.currentIndex()].getData()[1][int(BxPos):int(AxPos)]
                    self.MaxAB_input.setText(f"{np.max(MaxAB)}")
                    self.MinAB_input.setText(f"{np.min(MaxAB)}")
                else:
                    MaxAB = None
                    self.MaxAB_input.setText(f"None")
                    self.MinAB_input.setText(f"None")
        if self.counter_horizontal_cursor != 0:
            if self.counter_horizontal_cursor != 0:
                CyPos = self.lineC.getYPos()
                self.CyPos_input.setText(f"{round(CyPos, 2)}")
                if self.counter_horizontal_cursor == 2:
                    DyPos = self.lineD.getYPos()
                    self.DyPos_input.setText(f"{round(DyPos, 2)}")
                    if CyPos > DyPos:
                        Val_CD = CyPos - DyPos
                        self.Len_CD_input.setText(f"{round(Val_CD, 2)}")
                    elif CyPos < DyPos:
                        Val_CD = DyPos - CyPos
                        self.Len_CD_input.setText(f"{round(Val_CD, 2)}")
                
            

class MainWindow(QMainWindow):
    talking = Signal(int)
    def __init__(self):
        super().__init__()
        self._view()

        self.n_data = 160
        self.xdata = list(range(self.n_data))
        rows, cols = (5, 160)
        self.ydata = [[0 for i in range(cols)] for j in range(rows)]

        # its have to be here to give it abbility to have cusors and triggers

        self.plot = pg.PlotWidget()
        # self.plot.addItem(self.data_line[0],text = "chuj")
        self.pen = list()
        self.pen.append(pg.mkPen(color= (0,255,0), width = 3))
        self.pen.append(pg.mkPen(color= (255,0,0), width = 3))
        self.pen.append(pg.mkPen(color= (0,0,255), width = 3))
        self.pen.append(pg.mkPen(color= (255,255,0), width = 3))
        self.pen.append(pg.mkPen(color= (0,255,255), width = 3))

        self.data_line = list()
        self.data_line.append(pg.PlotCurveItem(self.xdata, self.ydata[0], pen=self.pen[0]))
        self.data_line.append(pg.PlotCurveItem(self.xdata, self.ydata[1], pen=self.pen[1]))
        self.data_line.append(pg.PlotCurveItem(self.xdata, self.ydata[2], pen=self.pen[2]))
        self.data_line.append(pg.PlotCurveItem(self.xdata, self.ydata[3], pen=self.pen[3]))
        self.data_line.append(pg.PlotCurveItem(self.xdata, self.ydata[4], pen=self.pen[4]))
        self.legend = pg.LegendItem()
       

        # RightBar is a class to show information like median or average also later can be used for sending data
        self.menu_bar = RightBar(self, self.plot, self.data_line)
        # self.showMaximized()
        self.newWindow = AnotherWindow("Plot Configuration", self)
        
        self._plotSetUp()
 
        self.worker = Worker(self)  # Worker
        self.worker_thread = QThread()  # Thread
        self._threadSetUp()
        
        self.timer = QTimer()
        self._timerSetUp()

        self.main_window_layout = QHBoxLayout()        
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
        
        self.worker.RecvMessage.connect(self.set_addData)
        self.talking.connect(self.worker.Talking)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        self.talking.emit(1)   

    def _plotSetUp(self):
        self.data_line[0].clear()
        self.legend.clear()
        self.plot.setBackground('w')
        if self.newWindow.plotlayouts[0].get_check() == True:
            self.plot.addItem(self.data_line[0])    
            self.legend.addItem(self.plot.getPlotItem().listDataItems()[0], self.newWindow.plotlayouts[0].get_name())
        elif self.newWindow.plotlayouts[0].get_check() != True:
            self.data_line[0].clear()
        if self.newWindow.plotlayouts[1].get_check() == True:
            self.plot.addItem(self.data_line[1])    
            self.legend.addItem(self.plot.getPlotItem().listDataItems()[1], self.newWindow.plotlayouts[1].get_name())
        elif self.newWindow.plotlayouts[1].get_check() != True:
            self.data_line[1].clear()
        if self.newWindow.plotlayouts[2].get_check() == True:
            self.plot.addItem(self.data_line[2])    
            self.legend.addItem(self.plot.getPlotItem().listDataItems()[2], self.newWindow.plotlayouts[2].get_name())
        elif self.newWindow.plotlayouts[2].get_check() != True:
            self.data_line[2].clear()
        if self.newWindow.plotlayouts[3].get_check() == True:
            self.plot.addItem(self.data_line[3])    
            self.legend.addItem(self.plot.getPlotItem().listDataItems()[3], self.newWindow.plotlayouts[3].get_name())
        elif self.newWindow.plotlayouts[3].get_check() != True:
            self.data_line[3].clear()
        if self.newWindow.plotlayouts[4].get_check() == True:
            self.plot.addItem(self.data_line[4])    
            self.legend.addItem(self.plot.getPlotItem().listDataItems()[4], self.newWindow.plotlayouts[4].get_name())
        elif self.newWindow.plotlayouts[4].get_check() != True:
            self.data_line[4].clear()
        self.plot.setXRange(0,160)
        self.plot.addItem(self.legend)
    def _add_plot(self, z):
        self.plot.addItem(self.data_line[z])

    def _remove_plot(self, z):
        self.plot.removeItem(self.data_line[z])

    def _timerSetUp(self):
        
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def _view(self):
        self.setWindowTitle("My App")
        self.setMinimumSize(400, 500)

    def _layoutoption(self):
        
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
        menubar.addAction("&Plot Configuration", lambda: self._show_new_window())
        menubar.addAction("&Send Message", lambda: self._send_new_window())
        self.setMenuBar(menubar)
    def _send_new_window(self):
        self.send_window = SendWindow()
        self.send_window.show()
        
    def _show_new_window(self):
        self.newWindow.show()
        self.menu_bar.button.click()
        # add refresh after window is closed

    def _buttonwork(self):

        print("button clicked!\nand it hurts!")

    def update_plot(self):
       
        tok = time.time()
       
        if self.menu_bar.get_button_status() == True:
            for i in range(len(self.newWindow.plotlayouts)):
                if self.newWindow.plotlayouts[i].get_check() == True:
                    self.data_line[i].setData(self.xdata, self.ydata[i])
            self.newWindow.close()

        tik = time.time()

        if (tik-tok) > 0.01:
            print(f"Failure to be fast enough: {tik-tok}")
    
    def set_addData(self, value = 0):
        
        if type(value) == list:
            for data in value:
                self.ydata[0].pop(0)
                self.ydata[0].append(data)
        elif type(value) == dict:
            for key, value in value.items():
                if str(key) == self.newWindow.plotlayouts[0].get_id() and True == self.newWindow.plotlayouts[0].get_check():
                    for data in value:
                        self.ydata[0].pop(0)
                        self.ydata[0].append(data)
                elif str(key) == self.newWindow.plotlayouts[1].get_id() and True == self.newWindow.plotlayouts[1].get_check():
                    for data in value:
                        self.ydata[1].pop(0)
                        self.ydata[1].append(data)
                elif str(key) == self.newWindow.plotlayouts[2].get_id() and True == self.newWindow.plotlayouts[2].get_check():
                    for data in value:
                        self.ydata[2].pop(0)
                        self.ydata[2].append(data)
                elif str(key) == self.newWindow.plotlayouts[3].get_id() and True == self.newWindow.plotlayouts[3].get_check():
                    for data in value:
                        self.ydata[3].pop(0)
                        self.ydata[3].append(data)
                elif str(key) == self.newWindow.plotlayouts[4].get_id() and True == self.newWindow.plotlayouts[4].get_check():
                    for data in value:
                        self.ydata[4].pop(0)
                        self.ydata[4].append(data)
                else:
                    #print("There are no Messages with those IDs or check is not marked")
                    pass
                
        else:
            self.addData = list()
            self.addData.append(value)
            self.ydata[0] = self.ydata[0][1:] + self.addData
    
    def get_ydata(self, z):
        return self.ydata[z]

    

       
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
    
    Mwindow.showMaximized()
    
    Mwindow.newWindow.show()
    status = app.exec()

    print(f"Program Finished with status: {status}")

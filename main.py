import os, sys, random
from PyQt5.QtCore import QSize, Qt, QTimer 
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QHBoxLayout, QMenu, QMenuBar,\
    QLabel, QLineEdit, QFormLayout
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import time
import sys
import numpy as np

debug = 0

def Average(data):
    value = 0
    if data != None:
        for i in data:
            value += i
    else:
        print("data is None")
    return (value/len(data))

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class RightBar(QWidget):

    def __init__(self, usecase):
        super().__init__()
        self.usecase = usecase
        self.button = QPushButton("Refresh")
        
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
        self.button.setCheckable(True)
        self.button.setChecked(True)
        self.button.setMinimumSize(150, 30)
        #self.button.setAligment(Qt.AlignRight)

    def _layoutoption(self):

        self.layout = QFormLayout()
        # adding widgets
        self.layout.addRow(self.button)
        self.layout.addRow(self.average, self.average_input)
        self.layout.addRow(self.median, self.median_input)
        self.layout.addRow(self.max, self.max_input)
        self.layout.addRow(self.min, self.min_input)
        
        
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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setMinimumSize(400, 500)

        # RightBar is a class to show information like median or average also later can be used for sending data
        self.menu_bar = RightBar(self)

        self.plot = MplCanvas(self, 5, 4, 100)
        
        self.set_ndata()

        self.ydata = [random.random()*10 for i in range(self.n_data)]
        
        self.update_plot()

        self.timer = QTimer()
        self.timer.setInterval(400)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()


       

        self._layoutoption()

        # Setting Widget for layout to show in center still don't know to make toolbar
        widget = QWidget()
        widget.setLayout(self.main_window_layout)

        # creating menu bar at top of the app
        self._menumake()
        self.setCentralWidget(widget)

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
        filemenu.addAction("Save", lambda: print("Plot saved"))
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
        self.set_addData(1,0)
        self.xdata = list(range(self.n_data))

        if debug == 1:
            print(type(self.addData))
        
        

        self.plot.axes.cla()

        self.plot.axes.plot(self.xdata, self.ydata, "g")
        if debug == 1:
            print(self.ydata)
        
        if self.menu_bar.get_button_status() == True:
            self.plot.draw()
        else:
            if debug == 1:
                print("Refresh is off")
        tik = time.time()
        if (tik-tok) > 0.4:
            print(f"Failure to be fast enough: {tik-tok}")
        
    def get_ydata(self):
        return self.ydata
    def set_addData(self, rand = 0, value = 0):
        
        self.addData = list()
        if rand == 1:
            self.addData.append(random.random()*10)
        else:
            self.addData.append(value)

        self.ydata = self.ydata[1:] + self.addData

    def set_ndata(self, value = 150):
        self.n_data = value
        


if __name__ == '__main__':

    app = QApplication(sys.argv)

    Mwindow = MainWindow()
    Mwindow.show()
    status = app.exec()

    print(f"Program Finished with status: {status}")

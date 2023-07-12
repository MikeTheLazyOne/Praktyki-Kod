import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QProgressBar
from PyQt5.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
import time


class Worker(QObject):
    RecvMessage = Signal(list)

    @Slot(int)
    def Talking(self,v):
        print("talk talk")
        os.system('sudo ip link set can0 type can bitrate 100000')
        os.system('sudo ifconfig can0 up')

        can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native

        msg = can0.recv(1)
       
        tok = time.time()
        list_to_send = list(range(5))
        while (v == 1):
   
            msg = can0.recv(1)
           
            lista = list()
           
            if msg is None:
                tik = time.time()

               
               
       
                self.RecvMessage.emit(lista)
                print(f'Timeout occurred, no message.Time since last message:{tik-tok}')
            else:
                tok = time.time()
               
                for i in range(int(msg.dlc/2)):
                   
                    num = decoding(msg.data[(i*2)+0],msg.data[(i*2)+1])
                   
                    lista.append(num)
                    list_to_send = list_to_send[1:] + lista
                   
                self.RecvMessage.emit(lista)    
                print(f"List to send = {list_to_send}")

        os.system('sudo ifconfig can0 down')
class MainWindow(QMainWindow):
    work_requested = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setGeometry(100, 100, 300, 50)
        self.setWindowTitle('QThread Demo')

        # setup widget
        self.widget = QWidget()
        layout = QVBoxLayout()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)       

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)

        self.btn_start = QPushButton('Start', clicked=self.start)

        layout.addWidget(self.progress_bar)
        layout.addWidget(self.btn_start)

        self.worker = Worker()
        self.worker_thread = QThread()

        self.work_requested.connect(self.worker.Talking(1))
        self.worker.RecvMessage.connect(self.set_addData)

        # move worker to the worker thread
        self.worker.moveToThread(self.worker_thread)

        # start the thread
        self.worker_thread.start()

        # show the window
        self.show()

    def start(self):
        self.btn_start.setEnabled(False)
        
        self.work_requested.emit(1)

    def set_addData(self, value = 0):
       
        print(f"value = {value}")
        self.addData = list()
        self.addData.append(value)

        self.ydata = self.ydata[1:] + self.addData


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
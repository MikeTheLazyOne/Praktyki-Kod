import os, time, can
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def twos_complement(x):
    
    if x<0 and x > -127:
        x = ~x
        x = x+129
        return (bin(x))
    elif (x < -127):
        print("Error invalid value")
        return(bin(0))
    elif(x<128):
        return (bin(x))
    
def reverse_twos_complement(x):
    if type(x) != int:
        x = int(x, 2)
    if x >=128:
        x = x-129
        x = ~x
    return x

def podziel_liste(lista, rozmiar):
    return[lista[i:i+rozmiar] for i in range(0,len(lista), rozmiar)]

def odpakowacz(x, y):
    x = str(x)
    y = str(y)
    num = (x+"."+y)
    
    return float(num)


os.system('sudo ip link set can0 type can bitrate 100000')
os.system('sudo ifconfig can0 up')

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native

#msg = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5, 6, 7], is_extended_id=False)
msg = can0.recv(1)
counter = 0
tok = time.time()

list_to_plot = list(range(160))


xdata = list(range(160))

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylim(-1,1)
line1, =ax.plot(xdata,list_to_plot)

while (True):
    
    msg = can0.recv(1)
    
  
    
    if msg is None:
        tik = time.time()
        print(f'Timeout occurred, no message.Time since last message:{tik-tok}')
    else:
        tok = time.time()
        #num_of_data = int(msg.dlc/2)
        for i in range(int(msg.dlc/2)):
            
            num = reverse_twos_complement(msg.data[(i*2)+0])
            dec = reverse_twos_complement(msg.data[(i*2)+1])
            element = odpakowacz(num, dec)
            
            lista = list()
            lista.append(element)
            list_to_plot = list_to_plot[1:] + lista
        print(msg)
                
    line1.set_ydata(list_to_plot)
    
    fig.canvas.draw()
    fig.canvas.flush_events()
    
    
    
    
    
    if msg == None:
        counter += 1
    else:
        counter = 0
    
    
   
    
os.system('sudo ifconfig can0 down')
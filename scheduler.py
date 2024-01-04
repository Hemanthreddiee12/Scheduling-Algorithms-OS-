
import matplotlib.pyplot as plt 
import numpy as np
import copy
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.interactive(True)


def browse_input():
    filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
    
    # go update list
    if(filename==''):
        filename='This path is not working.'
    else:
        i = 0
        data.clear()
        file = open(filename, "r")
        for line in file:
            endl = line.find('\n')
            if endl != -1 :
                line = line[:endl]
            if i == 0:
                pnum = line
            else:
                line = line.split(' ')
                # Process No.  ( Arriv , Runing , Priority )
                data[int(line[0])] = [float(line[1]),float(line[2]),float(line[3])]
            i+=1
        file.close()
        
    path_label.config(text=filename)
    update_graph()
    return


def DO_FCFS():
    output.clear()
    X_time.clear()
    Y_prun.clear()
    sorted_data = sorted(data.items(), key=lambda kv: kv[1])
    # Process No.  ( Arriv , Runing , Priority )
    AccumTime = 0
    prevX = 0
    prevY = 0
    for p in sorted_data:
        # P.Arriv
        pno = int(p[0])
        arrival = float(p[1][0])
        burst = float(p[1][1])
        
        if (arrival > prevX):
            X_time.append(prevX)
            Y_prun.append(0)
            X_time.append(arrival)
            Y_prun.append(0)
            X_time.append(arrival)
            Y_prun.append(pno)
            X_time.append(burst+arrival)          
            Y_prun.append(pno)
            #X_time.append(burst+arrival)          
            #Y_prun.append(0)
            prevX = arrival+burst
        else:
            X_time.append(prevX)
            Y_prun.append(pno)
            X_time.append(prevX+burst)          
            Y_prun.append(pno)
            prevX = prevX+burst
            
        output[pno] = [(prevX-arrival-burst),(prevX-arrival),(prevX-arrival)/burst]
        
    X_time.append(prevX)
    Y_prun.append(0)
    return
    
    
def update_graph():
    # Figure 
    figure = Figure(figsize=(13, 5), dpi=100)
    plot = figure.add_subplot(1, 1, 1)
    
    # Fetch selected algorithm
    ALGORITHM = algo.cget("text")
    if ALGORITHM=="HPF":
        DO_HPF()
    elif ALGORITHM=="FCFS":
        DO_FCFS()
    elif ALGORITHM=="RR":
        DO_RR()
    elif ALGORITHM=="SJF":
        DO_SJF()     
    elif ALGORITHM=="SRTF":
        DO_SRTF()
    
    # Draw Output
    plot.set_title (algo.cget("text"), fontsize=16)
    plot.set_ylabel("Process No.", fontsize=14)
    plot.set_xlabel("Time", fontsize=14)
    
    x = X_time
    y = Y_prun
    plot.step(x, y, color="red", linestyle="-")
    plot.grid(which='major', color='#AAAAAA', linestyle='-')
    plot.set_yticks(y)
    plot.set_xticks(x)
    canvas = FigureCanvasTkAgg(figure, root)
    canvas.get_tk_widget().grid(row=4, column=0,padx=5, pady=5,columnspan=4, sticky="news")

    return
    
def DO_HPF():
    output.clear()
    X_time.clear()
    Y_prun.clear()
    # Sorting with respect to Arrival Time
    sorted_data = sorted(data.items(), key=lambda kv: kv[1][0])
    pnum = len(sorted_data)
    
    # Process No.  ( Arriv , Runing , Priority )
    AccumTime = sorted_data[0][1][0]
    prevX = 0
    j = 0
    Queue = []

    for i in range(pnum):
        while j < pnum and sorted_data[j][1][0] <= AccumTime:
            Queue.append(sorted_data[j])
            j += 1

        if not Queue:
            p = sorted_data[i]
        else:
            # Select process with the highest priority
            Queue.sort(key=lambda kv: kv[1][2])
            p = Queue.pop(0)

        pno = p[0]
        arrival = p[1][0]
        burst = p[1][1]

        if arrival > prevX:
            X_time.append(prevX)
            Y_prun.append(0)
            X_time.append(arrival)
            Y_prun.append(0)
            X_time.append(arrival)
            Y_prun.append(pno)
            X_time.append(burst + arrival)
            Y_prun.append(pno)
            prevX = arrival + burst
        else:
            X_time.append(prevX)
            Y_prun.append(pno)
            X_time.append(prevX + burst)
            Y_prun.append(pno)
            prevX = prevX + burst

        output[pno] = [(prevX - arrival - burst), (prevX - arrival), (prevX - arrival) / burst]
        AccumTime = prevX

    X_time.append(prevX)
    Y_prun.append(0)
    return

def DO_RR():
    output.clear()
    X_time.clear()
    Y_prun.clear()
    QUANTM = quantum_val.get()    
    # Sorting w.r.t Arrival Time
    datacpy = copy.deepcopy(data)
    sorted_data = sorted(datacpy.items(), key=lambda kv: kv[1][0])
    pnum = len(sorted_data)    
    # Process No.  ( Arriv , Runing , Priority )
    prevX = sorted_data[0][1][0]
    j = 1
    RRQ = []    
    RRQ.append(sorted_data[0])
    while len(RRQ) != 0:
        if len(RRQ) == 0 and j < pnum:
            p = sorted_data[j]
            j += 1
        else:
            p = RRQ.pop(0)
        
        pno = p[0]
        arrival = p[1][0]
        burst = p[1][1]
        
        if arrival > prevX:
            X_time.append(prevX)
            Y_prun.append(0)
            
            X_time.append(arrival)
            Y_prun.append(0)
            
            X_time.append(arrival)
            Y_prun.append(pno)
            
            if burst > QUANTM:
                X_time.append(arrival + QUANTM) 
                prevX = arrival + QUANTM
            else:
                X_time.append(arrival + burst) 
                prevX = arrival + burst
            Y_prun.append(pno)
            
        else:
            X_time.append(prevX)
            Y_prun.append(pno)
            if burst >= QUANTM:
                X_time.append(prevX + QUANTM) 
                prevX = prevX + QUANTM
            else:
                X_time.append(prevX + burst) 
                prevX = prevX + burst
            Y_prun.append(pno)
        
        if burst > QUANTM:
            p[1][1] -= QUANTM
            RRQ.append(p)
        else:
            p[1][1] = 0
            p = data[int(pno)]
            arrival = p[0]
            burst = p[1]
            output[pno] = [(prevX - arrival - burst), (prevX - arrival), (prevX - arrival) / burst]

        if len(RRQ) == 0 and j < pnum:
            RRQ.append(sorted_data[j])
            j += 1

    X_time.append(prevX)
    Y_prun.append(0)

def DO_SJF():
    output.clear()
    X_time.clear()
    Y_prun.clear()
    # Sorting w.r.t Arrival Time and Burst Time
    datacpy = copy.deepcopy(data)
    sorted_data = sorted(datacpy.items(), key=lambda kv: (kv[1][0], kv[1][1]))
    pnum = len(sorted_data)
    
    # Process No.  ( Arriv , Runing , Priority )
    prevX = sorted_data[0][1][0] if pnum > 0 else 0
    j = 1
    RRQ = []    
    RRQ.append(sorted_data[0])
    
    while len(RRQ) != 0:
        while j < pnum and sorted_data[j][1][0] <= prevX:
            RRQ.append(sorted_data[j])
            j += 1

        RRQ = dict(RRQ)
        RRQ = sorted(RRQ.items(), key=lambda kv: kv[1][1])

        if len(RRQ) == 0 and j < pnum:
            p = sorted_data[j]
            j += 1
        else:
            p = RRQ[0]

        pno = p[0]
        arrival = p[1][0]
        burst = p[1][1]

        if arrival > prevX:
            X_time.append(prevX)
            Y_prun.append(0)

            X_time.append(arrival)
            Y_prun.append(0)

            X_time.append(arrival)
            Y_prun.append(pno)

            X_time.append(arrival + burst) if burst > 0 else X_time[-1]
            prevX = arrival + burst
            Y_prun.append(pno)

        else:
            X_time.append(prevX)
            Y_prun.append(pno)
            X_time.append(prevX + burst) if burst > 0 else X_time[-1]
            prevX = prevX + burst
            Y_prun.append(pno)

        if burst > 0:
            RRQ.pop(0)
            p[1][1] = 0
            output[pno] = [(prevX - arrival - burst), (prevX - arrival), (prevX - arrival) / burst]
            if len(RRQ) == 0 and j < pnum:
                RRQ.append(sorted_data[j])
                j += 1

    X_time.append(prevX)
    Y_prun.append(0)

    
def DO_SRTF():
    output.clear()
    X_time.clear()
    Y_prun.clear()
    QUANTM = quantum_val.get()    
    # Sorting with respect to Arrival Time
    datacpy = copy.deepcopy(data)
    sorted_data = sorted(datacpy.items(), key=lambda kv: kv[1][0])
    pnum = len(sorted_data)    
    # Process No.  ( Arriv , Runing , Priority )
    prevX = sorted_data[0][1][0]
    j = 1
    RRQ = []    
    RRQ.append(sorted_data[0])
    prevpid = 0
    dontswitch = 0
    while len(RRQ) != 0:
        while j < pnum and sorted_data[j][1][0] <= prevX:
            RRQ.append(sorted_data[j])
            j += 1
        
        RRQ = dict(RRQ)
        RRQ = sorted(RRQ.items(), key=lambda kv: kv[1][1])

        if len(RRQ) == 0 and j < pnum:
            p = sorted_data[j]
            j += 1
        else:
            p = RRQ[0]
        
        pno = p[0]
        arrival = p[1][0]
        burst = p[1][1]
        if arrival > prevX:
            X_time.append(prevX)
            Y_prun.append(0)
            
            X_time.append(arrival)
            Y_prun.append(0)
            
            X_time.append(arrival)
            Y_prun.append(pno)
            
            if burst > QUANTM:
                X_time.append(arrival + QUANTM) 
                prevX = arrival + QUANTM
            else:
                X_time.append(arrival + burst) 
                prevX = arrival + burst
            Y_prun.append(pno)
            
        else:
            X_time.append(prevX)
            Y_prun.append(pno)
            if burst >= QUANTM:
                X_time.append(prevX + QUANTM) 
                prevX = prevX + QUANTM
            else:
                X_time.append(prevX + burst) 
                prevX = prevX + burst
            Y_prun.append(pno)
        
        if p[1][1] > QUANTM:
            p[1][1] -= QUANTM
        else :
            RRQ.pop(0)
            p[1][1] = 0
            p = data[int(pno)]
            arrival = p[0]
            burst = p[1]
            output[pno] = [(prevX - arrival - burst), (prevX - arrival), (prevX - arrival) / burst]
            if len(RRQ) == 0 and j < pnum:
                RRQ.append(sorted_data[j])
                j += 1

    X_time.append(prevX)
    Y_prun.append(0)



def output_write():
    # Prompt the user to choose the file path
    output_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    if output_path:
        file = open(output_path, "w")
        pnum = len(output)
        file.write("Process Count : " + str(pnum) + '\n')
        avg_ta = 0
        avg_wta = 0
        file.write("P. No\t\t" + "Waiting time\t" + "T.A. time\t" + "W.T.A. time" + '\n')
        for i in output.keys():
            p = output[i]
            avg_ta += p[1]
            avg_wta += p[2]
            file.write(str(i) + "\t\t" + str(p[0]) + "\t\t" + str(p[1]) + "\t\t" + str(p[2]) + '\n')
        file.write("\nAvg. T.A. :" + str(avg_ta / pnum) + "\n" + "Avg. W.T.A. :" + str(avg_wta / pnum) + '\n')
        messagebox.showinfo("Output file status", "Successfully Written.")
        file.close()

    
 


# GLOBAL VARS
data = {}
output = {}

# Process Number/Count
pnum = 0

# Time slots
X_time = []
# Runing Process No.
Y_prun = []

root = Tk(className=' OS Scheduler')
#root.geometry("860x640")
#root.resizable(width=False, height=False)
filename=""


# Label-Input Time Quantum
quantum_label = Label(root,text='Quantum Time :')
quantum_label.grid(row=1 ,column=0,padx=12, pady=10,ipadx=5,sticky='w')
quantum_val = IntVar(root, value=1)

quantum_entry = Entry (root,textvariable=quantum_val)
quantum_entry.grid(row=1,column=1,ipadx=5,sticky="w")


# Show/Update Btn
update_btn = Button(root,text="Show/Update Graph",command=update_graph)
update_btn.grid(row=2,column=0,padx=5, pady=10,ipadx=5,columnspan=1,sticky='w')


# Open file Btn
browse_btn = Button(root,text="Select Input File",command=browse_input)
browse_btn.grid(row=3,column=0,padx=5,ipadx=19,columnspan=1,sticky='w')


# Show opened file path
file_label = Label(root,text='File Path: '+filename)
file_label.grid(row=5,column=0)

path_label = Label(root,text=filename)
path_label.grid(row=5,column=1)


# Drop down list for algorithm selection
OPTIONS = ["SELECT ALGORITHM","HPF","FCFS","RR","SJF","SRTF" ] 

variable = StringVar(root)
variable.set(OPTIONS[0]) # default value

algo = OptionMenu(root, variable, *OPTIONS)
algo.grid(row=2,column=1,sticky='w')

#Outputfile 
output_label = Label(root,text='Output file name :')
output_label.grid(row=3 ,column=1,sticky="w")
output_val = StringVar(root, value="Out.txt")

output_entry = Entry (root,textvariable=output_val)
output_entry.grid(row=3,column=2,sticky="w")

write_btn = Button(root,text="Write File",command=output_write)
write_btn.grid(row=3,column=3,padx=5,ipadx=19,columnspan=1,sticky='w')

# Graph
figure = Figure(figsize=(13, 5), dpi=100)
plot = figure.add_subplot(1, 1, 1)

plot.set_title (algo.cget("text"), fontsize=16)
plot.set_ylabel("Process No.", fontsize=14)
plot.set_xlabel("Time", fontsize=14)
x = X_time
y = Y_prun

plot.step(x, y, color="red", marker=".", linestyle="")
plot.grid(which='major', color='#AAAAAA', linestyle='-')
plot.set_yticks(y)
plot.set_xticks(x)

canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().grid(row=4, column=0,padx=5, pady=5,columnspan=4, sticky="news")

# Main loop

root.mainloop()
 
    

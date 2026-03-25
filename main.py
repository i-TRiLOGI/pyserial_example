import tkinter as tk
from tkinter import ttk
import serial, datetime
from serial.tools import list_ports

PARITY_MAP = {
    'None': serial.PARITY_NONE,
    'Odd': serial.PARITY_ODD,
    'Even': serial.PARITY_EVEN,
}
serialComm = serial.Serial()
ports = list_ports.comports()
portNames = [port.device for port in ports]

def setSerialComm():
    global serialComm
    serialComm = serial.Serial(
        port=portCombobox.get(),
        baudrate=int(baudCombobox.get()),
        bytesize=int(databitsCombobox.get()),
        stopbits=int(stopbitsCombobox.get()),
        parity=PARITY_MAP[parityCombobox.get()],
        timeout=int(timeoutEntry.get()) / 1000.0
    )

def openPort():
    global serialComm
    try:
        setSerialComm()
        if serialComm.is_open:
            printOutput("Opened port %s" % serialComm.port)
            openButton.config(state=tk.DISABLED)
            closeButton.config(state=tk.NORMAL)
    except Exception as e:
        print(e)
        printOutput("Failed to open port %s" % portCombobox.get())

def closePort():
    global serialComm
    try:
        if serialComm.is_open:
            serialComm.close()
            printOutput("Closed port %s" % serialComm.port)
            closeButton.config(state=tk.DISABLED)
            openButton.config(state=tk.NORMAL)
        else:
            printOutput("Port %s is already closed" % serialComm.port)
    except Exception as e:
        print(e)
        printOutput("Failed to close port %s" % portCombobox.get())

def printOutput(text):
    print(text)
    outputText.config(state="normal")
    line = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + text + "\n"
    outputText.insert(tk.END, line)
    outputText.config(state="disabled")

# Function to clear the output text
def clearOutput():
    outputText.config(state='normal')
    outputText.delete(1.0, tk.END)

def sendSerialCommand(event):
    global serialComm
    if not serialComm or not serialComm.is_open:
        printOutput("Port is not open")
        return
    command = commandEntry.get()
    bytes = (command + '\r').encode()
    try: 
        printOutput("Sending command %s" % command)
        serialComm.write(bytes)
        response = serialComm.read_until('\r')
        printOutput("Response: %s" % response.decode())
    except Exception as e:
        print(e)
        printOutput("Failed to send command %s" % command)

root = tk.Tk()
root.title("PLC Serial Port Communication")

# Row 1
frame1 = ttk.Frame(root)
frame1.pack(fill='x', padx=5, pady=5)

# Port Name
ttk.Label(frame1, text="Port Name:").pack(side='left', padx=(0, 5))
portCombobox = ttk.Combobox(
    frame1,
    values=portNames
)
portCombobox.pack(side='left', fill='x', expand=True, padx=(0, 10))
portCombobox.current(0)

# Baud Rate
ttk.Label(frame1, text="Baud Rate:").pack(side='left', padx=(10, 5))
baudCombobox = ttk.Combobox(
    frame1,
    values=[1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]
)
baudCombobox.pack(side='left', fill='x', expand=True)
baudCombobox.current(5)  # Default to 38400

# Row 2
frame2 = ttk.Frame(root)
frame2.pack(fill='x', padx=5, pady=5)

# Data Bits
ttk.Label(frame2, text="Data Bits:").pack(side='left', padx=(0, 5))
databitsCombobox = ttk.Combobox(frame2, values=[7, 8])
databitsCombobox.pack(side='left', fill='x', expand=True, padx=(0, 10))
databitsCombobox.current(1)  # Default to 8

# Stop Bits
ttk.Label(frame2, text="Stop Bits:").pack(side='left', padx=(10, 5))
stopbitsCombobox = ttk.Combobox(frame2, values=[1, 2])
stopbitsCombobox.pack(side='left', fill='x', expand=True)
stopbitsCombobox.current(0)  # Default to 1

# Row 3
frame3 = ttk.Frame(root)
frame3.pack(fill='x', padx=5, pady=5)

# Parity
ttk.Label(frame3, text="Parity:").pack(side='left', padx=(0, 5))
parityCombobox = ttk.Combobox(frame3, values=['None', 'Even', 'Odd'])
parityCombobox.pack(side='left', fill='x', expand=True, padx=(0, 10))
parityCombobox.current(0)  # Default to None

# Timeout
ttk.Label(frame3, text="Timeout (ms):").pack(side='left', padx=(10, 5))
defaultTimeoutVar = tk.StringVar(value="500")
timeoutEntry = ttk.Entry(frame3,  textvariable=defaultTimeoutVar)
timeoutEntry.pack(side='left', fill='x', expand=True)

# Row 4 - Buttons
frame4 = ttk.Frame(root)
frame4.pack(fill='x', padx=5, pady=5)

openButton = ttk.Button(frame4, text="Open Port", command=openPort)
openButton.pack(side='left', expand=True, padx=(0, 5))

closeButton = ttk.Button(frame4, text="Close Port", command=closePort)
closeButton.pack(side='left', expand=True, padx=(5, 0))
closeButton.config(state=tk.DISABLED)

# Row 5 - Command String
frame5 = ttk.Frame(root)
frame5.pack(fill='x', padx=5, pady=5)

ttk.Label(frame5, text="Command String (Press Enter to Send)").pack(anchor='w')
commandEntry = ttk.Entry(frame5)
commandEntry.pack(fill='x', pady=(0, 5))
commandEntry.bind("<Return>", sendSerialCommand)

# Row 6 - Output Text and Clear Button
frame6 = ttk.Frame(root)
frame6.pack(fill='both', expand=True, padx=5, pady=5)

# Output Text Widget
outputText = tk.Text(frame6, height=20, state='disabled')
outputText.pack(fill='both', expand=True)

# Clear Button Frame (to right-justify the button)
clearFrame = ttk.Frame(frame6)
clearFrame.pack(fill='x')

# Add the clear button, right-justified
clearButton = ttk.Button(clearFrame, text="Clear output")
clearButton.pack(side='right')
clearButton.config(command=clearOutput)

root.mainloop()

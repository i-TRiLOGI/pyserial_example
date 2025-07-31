# Serial Communication with PLC - Python Example

This is an example of how the Python PySerial library can be used to communicate with PLCs via an RS485 connection. The graphical user interface is defined via TKinter, which is included by default with Python installations on Windows, MacOS, and Linux.

## Prerequisites

Install these dependencies before executing this program:
* Latest version of Python 3. This should be preinstalled on MacOS and Linux. On Windows, I recommend installing Anaconda (Miniconda works if you find Anaconda too bloated)
* `pyserial` (can be installed via `pip install pyserial` from the command line)
* Any necessary device drivers if you use a USB UART adapter for serial communication

## Usage

1. Run `python main.py` which will launch the TKinter GUI in a separate window
2. Set your serial parameters (COM Port, baud rate, etc) as appropriate for your PLC
3. Click the `Open Port` button to establish the serial communication
4. Enter a command in the text field and press Enter. The response will display in the output text box underneath.

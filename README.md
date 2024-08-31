# srsinst.qcm

`srsinst.qcm` is a Python package to provide serial communication with the 
[QCM200, Quartz Crystall Microbalance](https://thinksrs.com/products/qcm200.html)
from [Stanford Research Systems (SRS)](https://thinksrs.com/).

`srsinst.qcm` uses [srsgui](https://pypi.org/project/srsgui/) package for the support of instrument communication and graphic user interface (GUI). 

![screenshot](https://github.com/thinkSRS/srsinst.qcm/blob/main/docs/_static/image/QCM200_screenshot.png?raw=true " ").

## Installation
You need a working Python 3.7 or later with `pip` (Python package installer) installed. 
If you don't, [install Python](https://www.python.org/) to your system.

To install `srsinst.qcm` as an instrument driver , use Python package installer `pip` from the command line.

    python -m pip install srsinst.qcm

To use it as a GUI application, create a virtual environment, 
if necessary, and install:

    python -m pip install srsinst.qcm[full]


## Run `srsinst.qcm200` as GUI application
If the Python Scripts directory is in your PATH environment variable,
start the application by typing from the command line:

    qcm

If not,

    python -m srsinst.qcm

will start the GUI application.

Once running the GUI, you can:
- Connect to a QCM200 from the Instruments menu.
- Select a task from the Task menu.
- Press the green arrow to run the selected task. 

You can write your own task(s) or modify an existing one and run it 
from the GUI application, too. For writing a task for the GUI application, 
refer the document on [srsgui package](https://thinksrs.github.io/srsgui/index.html).

## Use `srsinst.qcm` as instrument driver
* Start a Python interpreter, a Jupyter notebook, or an editor of your choice 
to write a Python script.
* Import the **QCM200** class from `srsinst.qcm` package.
* Create an instance of the **QCM200** and connect for the serial communication.


    C:\>python
    Python 3.8.3 (tags/v3.8.3:6f8c832, May 13 2020, 22:37:02) [MSC v.1924 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> 
    >>> from srsinst.qcm import QCM200
    >>> qcm = QCM200('serial', 'COM3', 9600)
    >>> qcm.check_id()
    ('QCM200', '136058', 'Rev0.91')


If you get the reply with *check_id()* method as shown above, 
you are ready to configure and acquire data from your QCM200.

The remote control and data acquisition of of QCM200 is simple: 
Select the gate time you want to use among 0.1s, 1.0s, and 10.0s;
check if a new set of frequency and resistance data is available; 
and read data.


    >>>  # Query the current date time
    >>> qcm.cmd.gate_time
    0.1
    >>>  # Change the gate time to 1.0 s
    >>> qcm.cmd.gate_time = 1.0
    >>> Check if the gate time is changed
    >>> qcm.cmd.gate_time
    1.0
    >>>  # Query frequency 
    >>> qcm.cmd.frequency
    4999699.7
    >>>  # Query resistance 
    >>> qcm.cmd.resistance
    13.756
    >>>

You can view all the commands available in the `cmd` component as following. 


    >>> qcm.cmd.dir
      {'components': {}, 
       'commands': {
           'id_string': ('QCMGetCommand', 'I'), 
           'display_mode': ('DictCommand', 'D'),  
           'frequency_scale': ('DictCommand', 'V'), 
           'gate_time': ('DictCommand', 'P'), 
           'frequency': ('QCMFloatGetCommand', 'F'), 
           'frequency_offset': ('FloatGetCommand', 'G'), 
           'resistance': ('QCMFloatGetCommand', 'R'), 
           'resistance_offset': ('FloatGetCommand', 'S'), 
           'status': ('QCMIntGetCommand', 'B'), 
           'timebase': ('DictCommand', 'T')}, 
       'methods': [
            'reset_frequency_offset', 
            'reset_resistance_offset']
       }
    >>>

For remote command details, refer to the  
[QCM200 manual Appendix B](https://www.thinksrs.com/downloads/pdfs/manuals/QCM200m.pdf#page=117).

Here is a simple, yet complete python script to acquire data from a QCM200
using `srsinst.qcm` package.


    import time
    from srsinst.qcm import QCM200
    
    GateTime = 1.0                             # Select among 0.1 s, 1.0 s, or 10 s
    DataAcquisitionTime = 600                  # Data collection time in seconds
                                               # Connect to a QCM
    qcm = QCM200('serial', 'COM3', 9600)       # For Linux systems, 'COM3' will be like '/dev/ttyUSB1'.
    qcm.cmd.gate_time = GateTime               # Set the gate time
    
    output_file = open('qcm-data.txt', 'wt')   # Open a file to write data
    
    time_elapsed = 0.0
    initial_time = time.time()
    
    while time_elapsed < DataAcquisitionTime:  
        time_elapsed = time.time() - initial_time
        new_data = qcm.get_data_if_both_new()  # Data available when Both F and R data are new.
        if new_data:
            data_format = f'{time_elapsed:7.2f} {new_data[0]:10.2f} {new_data[1]:7.3f}\n'
            output_file.write(data_format)
            print(data_format, end='')
            time.sleep(GateTime - 0.1)
            
    output_file.close()
    qcm.disconnect()        

The above Python script generates a series of (time, frequency, resistance) data tuples,
printed on the screen and saved into a file named 'qcm-data.txt'.


    0.00 4996689.10  13.861
    0.97 4996689.10  13.861
    2.03 4996689.10  13.859
    3.10 4996688.90  13.857
            .
            .
            .

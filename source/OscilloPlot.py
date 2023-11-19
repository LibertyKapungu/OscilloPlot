import csv
import os
import numpy as np
import PySimpleGUI as psg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class ChannelData:

    def __init__(self, filename, channel_number='Channel 1 x1'):
        
        self.filename = filename
        self.channel_num = channel_number
        self.label = f"Channel {self.channel_num} x1"

        self.tim_axis = []
        self.ampl_axis = []

        self.updated_ampl = []
        self.updated_time = []

        self.time_shift = 0.0
        self.amp_shift = 0.0
        self.time_scale = 1.0
        self.ampl_scale = 1.0

    def read_data(self):

        with open(self.filename, 'r') as csv_file:

            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip header

            for column in csv_reader:

                time = np.float64(column[3])
                ampl = np.float64(column[4])

                self.tim_axis.append(time)
                self.ampl_axis.append(ampl)

            self.amplitude_axis(1.0, 0.0)
            self.time_axis(1.0, 0.0)

        if not self.ampl_axis and not self.tim_axis:
            print('Channel ', self.channel_num, ' empty')    
        
    def amplitude_axis(self, scale=1.0, shift=0.0):
        self.updated_ampl = [value * scale + shift for value in self.ampl_axis]
        self.ampl_scale = scale
        self.label = f"{self.label[:self.label.index('x')]}" + f"x{self.ampl_scale}"

    def time_axis(self, scale = 1.0, shift = 0.0):
        
        self.updated_time = [time * scale + shift for time in self.tim_axis]
        self.time_scale = scale

class ChannelArray:
    def __init__(self):
        self.channel_array = {1: None, 2: None, 3: None, 4: None}

    def add_channel(self, filename, channel_number=1):
        self.channel_array[channel_number] = ChannelData(filename, channel_number)
        self.channel_array[channel_number].read_data()  # Call read_data() upon adding a new channel

#Array to hold all the channel objects
channel_array = ChannelArray()

def plot_channels(x_label = 'Time (s)', y_label = 'Magnitude', title = ' '):

    plt.clf()

    for i in range(1, 5):
        if channel_array.channel_array[i] is not None:
            plt.plot(channel_array.channel_array[i].updated_time, channel_array.channel_array[i].updated_ampl, label=channel_array.channel_array[i].label)

            print('Channel ', i, ' plotted successfully' )

    #Labels and titles      
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    plt.legend()

    plt.grid(True, which='both')
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='grey')
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.minorticks_on()

menu_def = [['Channel', ['Channel 1', 'Channel 2', 'Channel 3', 'Channel 4', 'Clear Channels']],
            ['Edit', ['Restore Defaults']],
            ['Help', 'About'],
            ]

layout = [
    [psg.Menu(menu_def)],

    [psg.Text('Scaling', font=('Any-Bold-Font', 15))],

    [psg.Text('Channel 1: '), psg.InputText(default_text='1', key='volts_scale_1')], [psg.Text('Channel 2: '), psg.InputText(default_text='1', key='volts_scale_2')],
    [psg.Text('Channel 3: '), psg.InputText(default_text='1', key='volts_scale_3')], [psg.Text('Channel 4: '), psg.InputText(default_text='1', key='volts_scale_4')],
    
    [psg.Text('Amplitude Shifting', font=('Any-Bold-Font', 15))],

    [psg.Text('Channel 1: '), psg.InputText(default_text='0.0', key='volts_shift_1')], [psg.Text('Channel 2: '), psg.InputText(default_text='0.0', key='volts_shift_2')],
    [psg.Text('Channel 3: '), psg.InputText(default_text='0.0', key='volts_shift_3')], [psg.Text('Channel 4: '), psg.InputText(default_text='0.0', key='volts_shift_4')],

    [psg.Text('Labels', font=('Any-Bold-Font', 15))],

    [psg.Text('X Label: '), psg.InputText(default_text='Time (s)', key='x_title')],
    [psg.Text('Y Label: '), psg.InputText(default_text='Magnitude (V)', key='y_title')],
    [psg.Text('Title: '), psg.InputText(default_text='OscilloPlot', key = 'title')],

    [psg.Button('Plot Channels', font=('Any-Bold-Font', 15))],

    [psg.Output(size=(80, 20))]
]

window = psg.Window("OscilloPlot", layout, default_element_size=(15, 1), auto_size_text=False, auto_size_buttons=False, default_button_element_size=(12, 1))

while True:

    event, values = window.read()

    if event == psg.WINDOW_CLOSED or event == 'Exit':
        break 

    elif event == 'About':
        psg.popup('About this program', 'Version 1.0.0', 'Plotting data from CSV files obtained from the oscilloscope.')

    elif event == 'Clear Channels':

        for i in range(1,5):

            channel_array.channel_array[i] = None

            volts_scale_key = f'volts_scale_{i}'
            ampl_shift_key = f'volts_shift_{i}'

            window[volts_scale_key].update(value = '1.0')
            window[ampl_shift_key].update(value = '0.0')

    elif event == 'Restore Defaults':

        for i in range(1,5):

            volts_scale_key = f'volts_scale_{i}'
            ampl_shift_key = f'volts_shift_{i}'

            window[volts_scale_key].update(value = '1.0')
            window[ampl_shift_key].update(value = '0.0')

        window['x_title'].update(value = 'Magnitude (V)')
        window['y_title'].update(value = 'Time (s)')
        window['title'].update(value = 'OscilloPlot')

    elif event in ['Channel 1', 'Channel 2', 'Channel 3', 'Channel 4']:

        ch_number = int(event.split()[-1])
        ch_file = psg.popup_get_file(f'{event} file', no_window=False)

        if ch_file:
            ch_name = os.path.abspath(ch_file)
            channel_array.add_channel(ch_name, ch_number)
            print(f'{channel_array.channel_array[ch_number].label} loaded successfully.')

        elif not ch_file:
            print('Channel ',ch_number, ' not loaded')

    elif event == 'Plot Channels':
        
        x_label = values['x_title']
        y_label = values['y_title']
        title = values['title']

        for i in range(1, 5):

            if channel_array.channel_array[i] is not None:
                volts_scale_key = f'volts_scale_{i}'
                ampl_shift_key = f'volts_shift_{i}'


                try:
                    amplitude_shift = float(values[ampl_shift_key])
                except:
                    amplitude_shift = 0.0
                    print('~ Invalid shift Input: default 0.0')
            
                try:
                    volts_scale = float(values[volts_scale_key])
                except:
                    volts_scale = 1.0
                    print('~ Invalid scale Input: default 1.0')

                channel_array.channel_array[i].amplitude_axis(volts_scale, amplitude_shift)

        plot_channels(x_label, y_label, title)
        plt.show()

window.close()

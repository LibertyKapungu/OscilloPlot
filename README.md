# Oscilloscope Data Plotter

![Project Image](project_images/main_image.svg)

This Python script, `OscilloPlot.py`, generates plots from oscilloscope data stored in CSV files. It provides users the capability to visualize up to four channels simultaneously, scale and shift the amplitude, and customize plot attributes like title, x-label, and y-label.

## Features

- **Multi-Channel Plotting:** Visualize up to four channels of oscilloscope data on a single plot.
- **Amplitude Scaling:** Scale the amplitude of the data for better visualization.
- **Amplitude Shifting:** Shift the amplitude of the data to focus on specific ranges.
- **Customization:** Set custom titles, x-labels, and y-labels for the generated plots.

## Usage

1. **Data Preparation:**
    - Ensure your oscilloscope data is stored in CSV file format.
    - Each CSV file should represent a single channel of data.
   
2. **Interactive Plotting:**
    - Use the on-screen options to adjust amplitude scaling and shifting.
    - Customize the plot title, x-label, and y-label as needed.

## Project Background

This tool was developed as part of an electronics project for creating a lightning and thunder detector. The ability to visualize oscilloscope data aided in analyzing and understanding electrical signals captured during the detector's operation.

## Dependencies

This script relies on the following Python libraries:

- `csv`: Included in the Python standard library for handling CSV files.
- `os`: Included in the Python standard library for operating system-related functions.
- `numpy`: Provides support for numerical operations and arrays.
- `PySimpleGUI`: Offers a simple and intuitive GUI interface.
- `matplotlib`: Used for plotting data and generating visualizations.


Before running the `OscilloPlot.py` script, ensure these dependencies are installed in your Python environment. You can install any missing libraries using pip by executing the respective `pip install`.

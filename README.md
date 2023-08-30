# VNAController

## Description

In the `vna_controller.py` file, you will find classes that facilitate interaction with the Planar TR1300/1. This Python code can serve as a tool within larger Python programs and was initially developed as a standalone Python module.

## Instrument

**Supported Instrument:** [Planar TR1300/1 2-Port 1.3 GHz Analyzer](https://coppermountaintech.com/vna/tr1300-1-2-port-1-3-ghz-analyzer/)

## Dependencies

### Python Libraries

- pyvisa
- pyvisa-py
- numpy

### Software

- [TRVNA Software](https://coppermountaintech.com/download-free-vna-software/)

## Operating System

- Windows

## Installation

To incorporate this module into a Python project:

1. Copy the `vna_controller.py` file to your computer.
2. Install the required Python libraries mentioned above and TRVNA.
3. Insert `vna_controller.py` into the current directory of your Python project.
4. Launch TRVNA. (System -> Misc Setup -> Network Setup -> TCP SOCKET ON)
5. Execute your Python project.

## GNU Radio

To integrate VNAController with GNU Radio:

1. Install the required Python libraries within GNU Radio by opening the Conda Prompt and navigating to the `radioconda` directory. Then install the libraries using the command `pip install lib_name`.
2. Launch GNU Radio and add a Python block to your flowgraph.
3. Edit the block, then copy the code from `vna_controller.py` above the script in the block.
4. Get creative with your designs and applications!

## Basic Usage Examples

Here are some basic examples demonstrating the usage of the `VNAController`:

```python
# Create an instance of VNAController
vna_controller = VNAController()

# Set the default format to Log Mag of S11
vna_controller.set_format()

config = RFConfig()

vna_controller.set_RFConfig(config)

# Perform an acquisition for S11
S11_data = vna_controller.acquisition()

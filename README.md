# SpiShell

Picture this: You just bought a cool new sensor and want to play around with it. But it only offers an SPI interface so now you need to go through your electronics box to find a vacant microcontroller, write a program that does a few SPI exchanges, compile it and flash it only to see one simple action before you have to do it again. Sucks right?
That's why this project offers an interactive shell for reading and writing data over SPI.

## Backends

The project offers different SPI backends:

- **FT232H**: Communication via a FTDI FT232H breakout board
- **RPi**: Communication via a Raspberry Pi's SPI pins
- **Mock**: Exists for development purposes, doesn't do actual data transfers

A backend needs to be specified as a parameter at launch. If none is given, it defaults to _Mock_.

## Modules

More complex behavior can be abstracted by implementing a module for a chip.
These modules can for one define variables that can be used with a preceding `$` in the shell.
They can also define custom commands for the shell that do more complex operations than just a single read or write. A custom command could, for example, only modify a single register config bit, or do conditional writes based on other data.
A module needs to be placed within the _modules_ subdirectory and can then be imported with the `import [module_name]` command.
An examplatory module definition is provided as `my_sensor.py`.

## Usage

Run `spishell/cli.py` with your favorite python interpreter that is version 3.10 or newer.
To get a list of available commands, run `help`.

## Installation

Problem for another day.

## ToDo

- Implement Raspberry Pi Backend
- Make use of SpiInterface parameters to choose from different devices
- Fix pylint import errors
- Create setup.py
- More detailed help for commands
- Split help section by module
- Implement an actual sensor

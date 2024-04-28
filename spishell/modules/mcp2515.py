'''
Module for interfacing with the MCP2515 CAN controller
'''
from enum import Enum
# pylint: disable=import-error
from registry import register_command

# TODO: make these variables availble in the shell? idk..

class Registers(Enum):
  '''
  Relevant SPI Registers
  '''
  CNF1 = 0b00101010
  CNF2 = 0b00101001
  CNF3 = 0b00101000
  CANCTRL = 0b00001111
  CANSTAT = 0b00001110

class Instructions(Enum):
  '''
  Relevant SPI Instructions
  '''
  RESET = 0b11000000
  READ = 0b00000011
  WRITE = 0b00000010

class OperationMode(Enum):
  '''
  Relevant operation modes.
  '''
  NORMAL = 0b000
  CONFIGURATION = 0b100


@register_command('reset')
def do_reset(spi, **_):
  '''Resets the MCP2515 to its default state.'''
  spi.exchange([Instructions.RESET.value])

@register_command('change_mode')
def do_change_mode(spi, line):
  '''Changes the MCP2515's operation mode'''
  if not line or line.upper() not in OperationMode._member_names_:
    print(f"Please specify a valid mode: {[m.name for m in OperationMode]}")
    return

  curr_ctrl = spi.read_reg(Registers.CANCTRL.value)
  curr_mode = OperationMode((curr_ctrl & 0b11100000) >> 5)

  new_mode = OperationMode[line.upper()]
  new_reg = (curr_ctrl & 0b00011111) | (new_mode.value << 5)

  print(f"Switching from {curr_mode} to {new_mode}...")
  spi.write_reg(Registers.CANCTRL.value, new_reg)

# TODO: startup configuratoin
# - set bitrate
# - set mask
# - set filter
# - enable filter and link to fifo

# TODO: CAN read
# TODO: CAN write

'''
Abstracts several SPI backends into a single class.
'''
from enum import Enum, auto
from pyftdi.spi import SpiController

class SpiMode(Enum):
  '''Available SPI backends.'''
  FT232H = auto()
  RPI = auto()
  MOCK = auto()

class SpiInterface:
  '''Interface that provides primitive read/write operations.'''
  def __init__(self, mode: SpiMode, url="ftdi:///1", cs=0, spi_mode=0):
    self.mode = mode
    if mode == SpiMode.RPI:
      # Implement SPI via RPi GPIO, import only as needed
      raise NotImplementedError("Raspberry Pi SPI has yet to be implemented")
    elif mode == SpiMode.FT232H:
      spi = SpiController()
      spi.configure(url)
      self.device = spi.get_port(cs, mode=spi_mode)
    else:
      # Only mock transfers
      pass

  def write_reg(self, addr_str, value_str):
    '''Writes a value to a register.
    Address and value need to be provided as hex strings.'''
    # Set write bit (Is this the way for all devices? I doubt it...)
    addr = int(addr_str, 16) | 0x80
    value = int(value_str, 16)
    print(f"Writing {hex(value)} to {hex(addr)}")
    if self.mode == SpiMode.FT232H:
      self.device.exchange([addr, value], 2)

  def read_reg(self, addr):
    '''Reads a value from a register and prints it.'''
    print(f"Reading Register {addr}:")
    if self.mode == SpiMode.FT232H:
      result = self.device.exchange([int(addr, 16)], 1)
      print(f"Value: {hex(result[0])} ({bin(result[0])})")

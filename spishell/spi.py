'''
Abstracts several SPI backends into a single class.
'''
from enum import Enum, auto
from typing import Union, Iterable
from pyftdi.spi import SpiController

# TODO: this should be split up into different classes with a common interface
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

  def write_reg(self, addr: int, value: int):
    '''Writes a value to a register.
    Address and value need to be provided as hex strings.'''
    print(f"Writing {hex(value)} to {hex(addr)}")
    if self.mode == SpiMode.FT232H:
      self.device.exchange([addr, value])

  def read_reg(self, addr: int) -> int:
    '''Reads a value from a register and prints it.'''
    print(f"Reading Register {hex(addr)}:")
    if self.mode == SpiMode.FT232H:
      result = self.device.exchange([addr], 1)
      print(f"Value: {hex(result[0])} ({bin(result[0])})")
      return result
    elif self.mode == SpiMode.MOCK:
      return 0

  def exchange(self, out: Union[bytes, bytearray, Iterable[int]]=b'', readlen: int=0) -> bytes:
    print(f"Writing {[hex(b) for b in out]}")
    if self.mode == SpiMode.FT232H:
      result = self.device.exchange(out, readlen)
      print(f"Got back {[hex(b) for b in result]}")
      return result

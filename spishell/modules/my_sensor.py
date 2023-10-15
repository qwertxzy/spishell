'''
Example definition to demonstrate how new modules are added.
'''
from registry import register_command, register_variable

# Modules can be imported during runtime in the shell
# so anything that is put here will be executed upon import
print(f"Hello from {__file__}")

# In order to define a variable, the register_variable method can be used:
register_variable("myvar", "0xDEAD")
register_variable("myvartwo", "0xBEEF")

# To add a command, the register_command decorator can be used:
@register_command("do_this")
def do_this(**_):
  '''Demo command.'''
  print("I am doing this.")

# Commands can also be added with aliases to introduce shortcuts
@register_command("do_that", "dt")
def do_that(line, **_):
  '''Another demo command.'''
  print(f"I am doing that: {line}")

# Methods that are added to the command registry can have the following parameters:
#  - spi: an instance of the spi interface
#  - line: the rest of the line after the command for arg parsing
# They need to however include a **_ parameter to include possible unused parameters.

'''
Main command-line interface module.
Will run an input loop when executed.
'''
import sys
import traceback
import importlib
from difflib import get_close_matches
from string import Template
# pylint: disable=import-error
from registry import register_command, commands, command_aliases, variables
from spi import SpiInterface, SpiMode

SPI = None

def run_command(line):
  '''Runs a single input line.'''
  # Split line into command and optional args
  parts = line.split(' ', 1)
  if len(parts) == 1:
    command, args = parts[0], None
  else:
    command, args = parts

  # Resolve alias if present
  if command in command_aliases:
    command = command_aliases[command]

  # Throw error if command is not defined
  if command not in commands:
    print(f"Unknown command: {command}")
    return

  # Resolve possible variables in line variable
  if args:
    try:
      t = Template(args)
      args = t.substitute(variables)
    except KeyError as k:
      print(f"Unknown variable: {k.args[0]}")
      return

  # Get command & run
  function = commands[command]
  dict_args = {"spi": SPI, "line": args}

  try:
    function(**dict_args)
  except Exception:
    print(traceback.format_exc())

@register_command("quit", "q")
def quit_cmd(**_):
  '''Quits the program.'''
  sys.exit()

@register_command("help", "?")
def help_cmd(**_):
  '''Prints a list of commands and their docstring.'''
  print("This is the help. Here's all commands:")
  for (cname, cfunc) in commands.items():
    aliases = [alias for alias, name in command_aliases.items() if name == cname]
    print(f"{cname}{(18 - len(cname)) * ' '}{', '.join(aliases)}\t{cfunc.__doc__}")

@register_command("listvars", "lv")
def listvars(**_):
  '''Lists all defined variables.'''
  print("Variables:")
  for key, value in variables.items():
    print(f"{key} -> {value}")

@register_command("echo")
def echo(line, **_):
  '''Prints the input back to the user.'''
  print(line)

@register_command("read_register", "rr")
def read_reg(spi, line):
  '''Read a register.'''
  spi.read_reg(line)

@register_command("write_register", "wr")
def do_write_reg(spi, line):
  '''Write a register.'''
  (addr, value) = line.split()
  spi.write_reg(addr, value)

@register_command("import")
def import_module(line, **_):
  '''Imports a module from the \'module\' subdirectory.'''
  print(f"Importing module {line}")
  importlib.import_module(f"modules.{line}")

@register_command('reload')
def reload_module(line, **_):
  '''Reloads an imported module.'''
  module = importlib.import_module(f"modules.{line}")
  importlib.reload(module)

@register_command("debug")
def debug(**_):
  '''Starts the python debugger.'''
  # pylint: disable=forgotten-debug-statement
  breakpoint()


if __name__ == '__main__':
  mode = SpiMode.MOCK

  # Determine closest backend match
  if len(sys.argv) > 1:
    match = get_close_matches(sys.argv[1].capitalize(), [m.name for m in SpiMode], n=1, cutoff=0.2)
    if not match:
      print(f"Unknown SPI backend '{sys.argv[1]}'")
      print("Available backends:")
      for m in SpiMode:
        print(f"  {m.name}")
    else:
      mode = SpiMode[match[0]]
  print(f"SPI Backend: {mode.name}")
  SPI = SpiInterface(mode)

  while True:
    user_input = input(">")
    if not user_input:
      continue
    run_command(user_input)

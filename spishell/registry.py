'''
Provides a registry for commands and variables that the CLI module can use.
'''
# Dict command_name -> function_ref
commands = {}

# Dict alias -> command_name
command_aliases = {}

# Dict var_name -> value
variables = {}

# Decorator for adding functions
def register_command(name, *aliases):
  '''Registers a command with an optional list of aliases.'''
  def decorator(func):
    commands[name] = func
    for alias in aliases:
      command_aliases[alias] = name
    return func
  return decorator

# Method for adding variables
def register_variable(name, value):
  '''Registers a variable to be substituted with its value.'''
  variables[name] = value

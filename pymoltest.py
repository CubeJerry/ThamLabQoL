from pymol import cmd

def my_custom_command(arg1, arg2="default_value"):
    """
    DESCRIPTION:
        A custom PyMOL command that takes two arguments.
    USAGE:
        my_custom_command arg1_value, arg2_value
    PARAMETERS:
        arg1: The first argument (required).
        arg2: The second argument (optional, defaults to "default_value").
    """
    print(f"Argument 1: {arg1}")
    print(f"Argument 2: {arg2}")

# Extend PyMOL with your custom command
cmd.extend("my_custom_command", my_custom_command)

from templates.commands import cmd_help, cmd_start, cmd_test

START_MESSAGE = "Hello world!"

HELP_MESSAGE = "Hello world! \n\n " \
               "Available commands: \n" \
               f" /{cmd_start.command} - {cmd_start.description}\n" \
               f" /{cmd_help.command} - {cmd_help.description}\n" \
               f" /{cmd_test.command} - {cmd_test.description}"

from templates.commands import cmd_help, cmd_start, cmd_test


MSG_THROTTLING_MIDDLEWARE = "You are too fast, please wait a little"

START_MESSAGE = "Hello world!"

HELP_MESSAGE = "Hello world! \n\n " \
               "Available commands: \n" \
               f" /{cmd_start.command} - {cmd_start.description}\n" \
               f" /{cmd_help.command} - {cmd_help.description}"

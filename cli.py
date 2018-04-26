
#!/usr/bin/env python

""" User registers commands with CommandGroups """

import os
import sys
from collections import OrderedDict

from knack import CLI
from knack.commands import CLICommandsLoader, CommandGroup
from knack.arguments import ArgumentsContext
from knack.help import CLIHelp

from knack.help_files import helps

import handler

cli_name = os.path.basename(__file__)

helps['create'] = """
    type: group
    short-summary: create deployment.
"""

helps['create deployment'] = """
    type: command
    short-summary: create deployment.
    examples:
        - name: It's pretty straightforward.
          text: {cli_name} create deployment --path "source_files_path"
""".format(cli_name=cli_name)


def create_command_handler(path, namespace, repo_url, folders, repo_name, with_draft):

    commands_handler = handler.Handler()
    charts_details = commands_handler.get_helm_charts_details(repo_name, repo_url, folders)
    files = commands_handler.get_source_files(path)
    
    commands_handler.install_helm_chart("mysql", "stable/mysql", namespace)
    
WELCOME_MESSAGE = r"""
 _        _______  _______  _______ _________ _______ 
| \    /\(  ____ )(  ____ \(  ___  )\__   __/(  ____ \
|  \  / /| (    )|| (    \/| (   ) |   ) (   | (    \/
|  (_/ / | (____)|| (__    | (___) |   | |   | (__    
|   _ (  |     __)|  __)   |  ___  |   | |   |  __)   
|  ( \ \ | (\ (   | (      | (   ) |   | |   | (      
|  /  \ \| ) \ \__| (____/\| )   ( |   | |   | (____/\
|_/    \/|/   \__/(_______/|/     \|   )_(   (_______/

Welcome to the cool Kreate CLI!

Here are the base commands:
"""

class KreateCLIHelp(CLIHelp):

    def __init__(self, cli_ctx=None):
        super(KreateCLIHelp, self).__init__(cli_ctx=cli_ctx,
                                        privacy_statement='Kreate privacy statement.',
                                        welcome_message=WELCOME_MESSAGE)


class CommandsLoader(CLICommandsLoader):

    def load_command_table(self, args):
        with CommandGroup(self, 'create', '__main__#{}') as g:
            g.command('deployment', 'create_command_handler',
                      confirmation=False)
        return super(CommandsLoader, self).load_command_table(args)

    def load_arguments(self, command):
        with ArgumentsContext(self, 'create deployment') as ac:
            ac.argument('path', required=True)
            ac.argument('namespace', default="default",
                        const="default", nargs='?', required=False)
            ac.argument('repo_url', default="https://github.com/kubernetes/charts.git",
                        const="https://github.com/kubernetes/charts.git", nargs='?', required=False)
            ac.argument('folders', default=[
                        "stable", "incubator"], nargs='*', required=False)
            ac.argument('repo_name', default="charts",
                        const="charts", nargs='?', required=False)
            ac.argument('with_draft', default=False,
                        const=True, nargs='?', required=False)

        super(CommandsLoader, self).load_arguments(command)


kreate_cli = CLI(cli_name=cli_name,
            config_dir=os.path.join('~', '.{}'.format(cli_name)),
            config_env_var_prefix=cli_name,
            commands_loader_cls=CommandsLoader,
            help_cls=KreateCLIHelp)
exit_code = kreate_cli.invoke(sys.argv[1:])
sys.exit(exit_code)

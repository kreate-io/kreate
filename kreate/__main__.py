
#!/usr/bin/env python

""" User registers commands with CommandGroups """

import os
import sys
from knack import CLI
from knack.arguments import ArgumentsContext
from knack.commands import CLICommandsLoader, CommandGroup
from knack.help import CLIHelp
from knack.help_files import helps
from kreate import handler

cli_name = os.path.basename(__file__)

helps['deploy'] = """
    type: group
    short-summary: kreate deploy.
"""

helps['deploy'] = """
    type: command
    short-summary: deploy.
    examples:
        - name: It's pretty straightforward.
          text: {cli_name} deploy --path "source_files_path"
""".format(cli_name=cli_name)


def create_command_handler(path, namespace, repo_url, folders, repo_name, with_draft, dry_run):

    commands_handler = handler.Handler()
    commands_handler.download_models()
    charts = commands_handler.get_helm_charts_details(
        repo_name, repo_url, folders)
    files = commands_handler.get_source_files(path)
    matched_charts = commands_handler.match_source_to_charts(files, charts)

    for chart_group in matched_charts:
        commands_handler.install_helm_chart(
            chart_group[0]['fullname'], namespace, dry_run)


WELCOME_MESSAGE = r"""
 _        _______  _______  _______ _________ _______ 
| \    /\(  ____ )(  ____ \(  ___  )\__   __/(  ____ \
|  \  / /| (    )|| (    \/| (   ) |   ) (   | (    \/
|  (_/ / | (____)|| (__    | (___) |   | |   | (__    
|   _ (  |     __)|  __)   |  ___  |   | |   |  __)   
|  ( \ \ | (\ (   | (      | (   ) |   | |   | (      
|  /  \ \| ) \ \__| (____/\| )   ( |   | |   | (____/\
|_/    \/|/   \__/(_______/|/     \|   )_(   (_______/

Welcome to the Kreate CLI!

Here are the base commands:
"""


class KreateCLIHelp(CLIHelp):

    def __init__(self, cli_ctx=None):
        super(KreateCLIHelp, self).__init__(cli_ctx=cli_ctx,
                                            privacy_statement='', welcome_message=WELCOME_MESSAGE)


class CommandsLoader(CLICommandsLoader):

    def load_command_table(self, args):
        with CommandGroup(self, '', '__main__#{}') as g:
            g.command('deploy', 'create_command_handler',
                      confirmation=False)
        return super(CommandsLoader, self).load_command_table(args)

    def load_arguments(self, command):
        with ArgumentsContext(self, 'deploy') as ac:
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
            ac.argument('dry_run', default=False,
                        const=False, nargs='?', required=False)

        super(CommandsLoader, self).load_arguments(command)


kreate_cli = CLI(cli_name=cli_name,
                 config_dir=os.path.join('~', '.{}'.format(cli_name)),
                 config_env_var_prefix=cli_name,
                 commands_loader_cls=CommandsLoader,
                 help_cls=KreateCLIHelp)
exit_code = kreate_cli.invoke(sys.argv[1:])
sys.exit(exit_code)

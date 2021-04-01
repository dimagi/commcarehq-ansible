from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys
from textwrap import dedent

from clint.textui import indent

from commcare_cloud.alias import commcare_cloud
from commcare_cloud.cli_utils import ask, check_branch
from commcare_cloud.colors import color_notice, color_summary, color_warning
from commcare_cloud.commands import shared_args
from commcare_cloud.commands.ansible import ansible_playbook
from commcare_cloud.commands.ansible.helpers import AnsibleContext
from commcare_cloud.commands.command_base import Argument, CommandBase
from commcare_cloud.commands.deploy.commcare import deploy_commcare
from commcare_cloud.commands.deploy.formplayer import deploy_formplayer
from commcare_cloud.commands.terraform.aws import get_default_username
from commcare_cloud.environment.main import get_environment
from commcare_cloud.environment.paths import get_available_envs


class Deploy(CommandBase):
    command = 'deploy'
    help = (
        "Deploy CommCare"
    )

    arguments = (
        Argument('component', nargs='?', choices=['commcare', 'formplayer'], help="""
            The component to deploy. If not specified, will deploy CommCare, or
            both, if always_deploy_formplayer is set in meta.yml
        """),
        Argument('--resume', action='store_true', help="""
            Rather than starting a new deploy, start where you left off the last one.
        """),
        Argument('--skip-record', action='store_true', help="""
            Skip the steps involved in recording and announcing the fact of the deploy.
        """),
        Argument('--commcare-rev', help="""
            The name of the commcare-hq git branch, tag, or SHA-1 commit hash to deploy.
        """, default=None),
        Argument('--set', dest='fab_settings', help="""
            fab settings in k1=v1,k2=v2 format to be passed down to fab 
        """, default=None),
        shared_args.QUIET_ARG,
        shared_args.BRANCH_ARG,
    )

    def modify_parser(self):
        if len(sys.argv) <= 1:
            # No environment specified, so no need to add environment-specific repositories
            return

        env_name = sys.argv[1]
        if env_name not in get_available_envs():
            return

        environment = get_environment(env_name)
        if environment.meta_config.git_repositories:
            for repo in environment.meta_config.git_repositories:
                Argument('--{}-rev'.format(repo.name), help="""
                    The name of the git branch, tag, or SHA-1 commit hash to deploy for the
                    '{}' ({}) repository
                """.format(repo.name, repo.url)).add_to_parser(self.parser)

    def run(self, args, unknown_args):
        check_branch(args)
        environment = get_environment(args.env_name)

        deploy_component = args.component
        if deploy_component == None:
            deploy_component = 'both' if environment.meta_config.always_deploy_formplayer else 'commcare'

        if deploy_component in ['commcare', 'both']:
            if deploy_component != 'both':
                _warn_no_formplayer()
            return deploy_commcare(environment, args, unknown_args)
        if deploy_component in ['formplayer', 'both']:
            if deploy_component != 'both':
                if args.commcare_rev:
                    print(color_warning('--commcare-rev does not apply to a formplayer deploy and will be ignored'))
                if args.fab_settings:
                    print(color_warning('--set does not apply to a formplayer deploy and will be ignored'))
            return deploy_formplayer(environment, args)


def _warn_no_formplayer():
    print(color_notice(dedent("""
        Formplayer will not be deployed right now, but we recommend deploying
        formplayer about once a month as well.
        It causes about 1 minute of service interruption to Web Apps and App
        Preview, but keeps these services up to date.
        You can do so by running `commcare-cloud <env> deploy formplayer`
    """)))
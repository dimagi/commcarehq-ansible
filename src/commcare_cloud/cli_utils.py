from __future__ import absolute_import, print_function, unicode_literals

import re
import subprocess
import sys
from io import open

from clint.textui import puts
from six.moves import input, shlex_quote

from commcare_cloud.colors import color_code, color_error

from .environment.paths import ANSIBLE_DIR
from .environment.main import get_environment


def ask(message, strict=False, quiet=False):
    if quiet:
        return True
    yesno = 'YES/NO' if strict else 'y/N'
    negatives = ('NO', 'N', 'n', 'no', '')
    affirmatives = ('YES',) if strict else ('y', 'Y', 'yes')
    acceptable_options = affirmatives + negatives

    response = ask_option(message, yesno.split('/'), acceptable_options)
    return response in affirmatives


def ask_option(message, options, acceptable_responses=None):
    options_display = '/'.join(options)
    acceptable_responses = acceptable_responses or options
    r = input('{} [{}]'.format(message, options_display))
    while r not in acceptable_responses:
        r = input('Please enter one of {} :'.format(', '.join(options)))
    return r

def get_dev_username(env_name):
    from .commands.terraform.aws import (
        get_default_username,
        print_help_message_about_the_commcare_cloud_default_username_env_var,
    )

    environment = get_environment(env_name)
    username = default_username = get_default_username()
    while True:
        if not username or default_username.is_guess:
            username = input(f"Enter your SSH username ({default_username}): ")
            if not username:
                username = default_username
        if username in environment.users_config.dev_users.present:
            break
        allowed_users = environment.users_config.dev_users.present
        env_users = '\n  - '.join([''] + allowed_users)
        puts(color_error(
            f"Unauthorized user {username}.\n\n"
            f"Please pass in one of the allowed ssh users:{env_users}"
        ))
        username = ""
    if default_username.is_guess:
        print_help_message_about_the_commcare_cloud_default_username_env_var(username)
    return username

def has_arg(unknown_args, short_form, long_form):
    """
    check whether a conceptual arg is present in a list of command line tokens

    :param unknown_args: list of command line tokens
    :param short_form: dash followed by single letter, e.g. '-f'
    :param long_form: double dash followed by work, e.g. '--forks'
    :return: boolean
    """

    assert re.match(r'^-[a-zA-Z0-9]$', short_form)
    assert re.match(r'^--\w+$', long_form)
    if long_form in unknown_args:
        return True
    for arg in unknown_args:
        if arg.startswith(short_form):
            return True
    return False


def git_branch():
    # https://stackoverflow.com/a/19585361/10840
    try:
        git_status = subprocess.check_output(
            "git status",
            cwd=ANSIBLE_DIR,
            shell=True,
            stderr=open('/dev/null', 'w', encoding='utf-8'),
            universal_newlines=True,
        )
    except subprocess.CalledProcessError as e:
        if e.returncode == 128:
            # We are not in a git repo; most likely pip installed
            return None
        else:
            raise
    return git_status.splitlines()[0].strip().split()[-1]


def check_branch(args):
    branch = git_branch()
    if branch is None:
        # not in a git repo
        if args.branch != 'master':
            puts(color_error("You are not in a git repo. To deploy, remove --branch={}".format(branch)))
            exit(-1)
    elif args.branch != branch:
        puts(color_error("You are not currently on the branch specified with the --branch tag. To deploy on "
                         "this branch, use --branch={}, otherwise, change branches".format(branch)))
        exit(-1)


def print_command(command):
    """
    commcare-cloud commands by convention print the underlying command they execute

    Use this function to do so
    """
    if isinstance(command, (list, tuple)):
        command = ' '.join(shlex_quote(arg) for arg in command)
    print(color_code(command), file=sys.stderr)

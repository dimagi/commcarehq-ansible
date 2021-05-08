from github.GithubException import GithubException

from commcare_cloud.alias import commcare_cloud
from commcare_cloud.colors import color_summary, color_error
from commcare_cloud.commands.terraform.aws import get_default_username


def create_release_tag(environment, repo, diff):
    if environment.fab_settings_config.tag_deploy_commits:
        try:
            repo.create_git_ref(
                ref='refs/tags/{}-{}-deploy'.format(
                    environment.new_release_name(),
                    environment.name),
                sha=diff.deploy_commit,
            )
        except GithubException as e:
            print(color_error(f"Error creating release tag: {e}"))


def announce_deploy_start(environment, service_name, commcare_rev=None):
    user = get_default_username()
    env_name = environment.meta_config.deploy_env
    subject = f"{user} has initiated a {service_name} deploy to {env_name}"
    if commcare_rev:
        subject = f"ATTENTION: {user} has initiated {service_name} deploy with branch {commcare_rev} to {env_name}"
    send_email(
        environment,
        subject=subject,
    )


def announce_deploy_failed(environment, service_name):
    send_email(
        environment,
        subject=f"{service_name} deploy to {environment.name} failed",
    )


def announce_deploy_success(environment, service_name, diff_ouptut):
    recipient = environment.public_vars.get('daily_deploy_email', None)
    send_email(
        environment,
        subject=f"{service_name} deploy successful - {environment.name}",
        message=diff_ouptut,
        to_admins=not recipient,
        recipients=[recipient] if recipient else None
    )


def send_email(environment, subject, message='', to_admins=True, recipients=None):
    """
    Call a Django management command to send an email.

    :param environment: The Environement object
    :param subject: Email subject
    :param message: Email message
    :param to_admins: True if mail should be sent to Django admins
    :param recipients: List of additional addresses to send mail to
    """
    if environment.fab_settings_config.email_enabled:
        print(color_summary(f">> Sending email: {subject}"))
        args = [
            message,
            '--subject', subject,
            '--html',
        ]
        if to_admins:
            args.append('--to-admins')
        if recipients:
            if isinstance(recipients, list):
                recipients = ','.join(recipients)

            args.extend(['--recipients', recipients])

        commcare_cloud(
            environment.name, 'django-manage', '--quiet', 'send_email',
            *args,
            show_command=False
        )

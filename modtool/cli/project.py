"""
Wrapper around various modding tools for SMB2
"""
import click
from project import SMBProject


@click.group()
def project():
    pass


@click.command()
@click.option(
    '--config',
    default='project.toml',
    help="Project config file"
)
def init(config):
    smb_project = SMBProject(config)
    smb_project.init()


@click.command()
@click.option(
    '--config',
    default='project.toml',
    help="Project config file"
)
def build(config):
    smb_project = SMBProject(config)
    smb_project.build()


@click.command()
@click.option(
    '--config',
    default='project.toml',
    help="Project config file"
)
def run(config):
    smb_project = SMBProject(config)
    smb_project.run()


project.add_command(init)
project.add_command(build)
project.add_command(run)

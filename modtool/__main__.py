"""
Wrapper around various modding tools for SMB2
"""
import click
from cli import project, util


@click.group()
def cli():
    pass


cli.add_command(util)
cli.add_command(project)


if __name__ == "__main__":
    cli()

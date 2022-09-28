"""
Wrapper around various modding tools for SMB2
"""
import click

from tools import PPCInject, ApeSphere


@click.group()
def util():
    pass


@click.group()
def project():
    pass


@click.command()
@click.argument('path')
@click.option(
    '--force',
    is_flag=True,
    default=False,
    help='Force a rebuild'
)
def setup_tools(path, force):
    ppcinject = PPCInject(f'{path}/ppc-inject')
    apesphere = ApeSphere(f'{path}/apesphere-custom')

    if not ppcinject.is_avaliable() or force:
        print("Building PPCInject")
        ppcinject.build()
    if not apesphere.is_avaliable() or force:
        print("Building ApeSphere-Custom")
        apesphere.build()


@click.command()
@click.option(
    '--tool-path',
    default='tools/',
    help='Path to find the tools'
)
@click.option(
    '--no-default-config',
    is_flag=True,
    default=False,
    help='Skip copying over a default configuration'
)
@click.argument('src')
@click.argument('dst')
def apesphere(src, dst, tool_path, no_default_config):
    # check tool avaliablity
    ppcinject = PPCInject(f'{tool_path}/ppc-inject')
    apesphere = ApeSphere(f'{tool_path}/apesphere-custom')

    if not (ppcinject.is_avaliable() or apesphere.is_avaliable()):
        print("Please run the `setup_tools` command first!")
        return

    config = {
        'ppcinject': f'{tool_path}/ppc-inject',
        'src': src,
        'dst': dst
    }

    if no_default_config:
        config['default_config'] = False

    apesphere.install(config)


util.add_command(setup_tools)
util.add_command(apesphere)

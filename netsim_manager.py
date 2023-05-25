#!/usr/bin/python3
from netsim_manager.manager import NetsimManager
import click

@click.group('cli')
@click.pass_context
@click.version_option()
def cli(ctx):
    ctx.obj = NetsimManager()

@cli.command('init')
@click.pass_context
def init(ctx):
    """Initialize netsim network"""
    ctx.obj.initialize_network()

@cli.command('onboard')
@click.pass_context
def onboard(ctx):
    """Onboard netsim devices on running NSO instance"""
    ctx.obj.onboard()

@cli.command('load')
@click.pass_context
def load(ctx):
    """Load day0 config for netsim devices"""
    ctx.obj.load()

@cli.command('save')
@click.pass_context
def save(ctx):
    """Save current config as day0 for devices"""
    ctx.obj.save()

@cli.command('list')
@click.pass_context
def list_devices(ctx):
    """List existing devices on current netsim managed instance"""
    ctx.obj.list_devices()

@cli.command('start')
@click.pass_context
def start(ctx):
    """Start current netsim instance"""
    ctx.obj.start()

@cli.command('stop')
@click.pass_context
def stop(ctx):
    """Stop current netsim instance"""
    ctx.obj.stop()

@cli.command('remove')
@click.pass_context
def remove(ctx):
    """Removes devices from running NSO instance"""
    ctx.obj.remove()

@cli.command('delete')
@click.pass_context
def delete(ctx):
    """Removes devices from running NSO instance"""
    ctx.obj.delete()

@cli.command('get-settings')
@click.pass_context
def get_settings(ctx):
    """Removes devices from running NSO instance"""
    ctx.obj.print_settings()

def main():
   cli(prog_name="cli")
 
if __name__ == '__main__':
   main()

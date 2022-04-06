#!/usr/bin/python3
# Author: Matheus Augusto da Silva
# Email:  a.matheus26@hotmail.com

import ruamel.yaml as yaml
import subprocess
import shutil
import click
import os

def get_config():
    with open('manager.yml','r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print("Error reading config file")
            raise exc
        return config

@click.group()
@click.version_option()
def cli():
    pass

@cli.command()
@click.option('--network', default='', help='Netsim network to create. Used as prefix')
@click.option('--num-devices', default=0, help='Integer (one or more)')
@click.option('--ned', default='', help='Integer (one or more)')
def destroy(network, num_devices, ned):
    """Removes config files from current directory."""
    current_dir = os.getcwd()
    config = get_config()

    # Read from config file if CLI arg wasn't specified
    if ned == '':
        ned    = config['ned']
    if network == '':
        network  = config['network']
    if num_devices == 0:
        num_devices  = config['num_devices']

    # Create directories for devices
    devices = [ f"{network}{index}" for index in range(num_devices) ]
    for device_name in devices:
        try:
            shutil.rmtree(os.path.join(current_dir, device_name))
        except OSError:
            pass

    shutil.rmtree(os.path.join(current_dir,network))
    os.remove(os.path.join(current_dir,'.netsiminfo'))

@cli.command()
@click.option('--network', default='', help='Netsim network to create. Used as prefix')
@click.option('--num-devices', default=0, help='Integer (one or more)')
@click.option('--ned', default='', help='Integer (one or more)')
def init(network, num_devices, ned):
    """Initializes netsim files in current directory."""
    current_dir = os.getcwd()
    config = get_config()

    # Read from config file if CLI arg wasn't specified
    if ned == '':
        ned    = config['ned']
    if network == '':
        network  = config['network']
    if num_devices == 0:
        num_devices  = config['num_devices']

    # Create directories for devices
    devices = [ f"{network}{index}" for index in range(num_devices) ]
    for device in devices:
        try:
            os.mkdir(os.path.join(current_dir, device))
        except OSError:
            pass

    # Initialize netsim locally
    result = subprocess.run(["ncs-netsim",
                            "--dir",f"{current_dir}",
                            "create-network",
                            f"{ned}",
                            f"{num_devices}",
                            f"{network}"])

@cli.command()
def start():
    """Start netsim devices."""
    current_dir = os.getcwd()

    # Initialize netsim locally
    result = subprocess.run(["ncs-netsim",
                            "start",])

@cli.command()
def stop():
    """Stop netsim devices."""
    current_dir = os.getcwd()

    # Initialize netsim locally
    result = subprocess.run(["ncs-netsim",
                            "stop",])

@cli.command()
def onboard():
    """Onboards Netsim devices to NSO."""
    current_dir = os.getcwd()
    config = get_config()

    # Read from config file
    ned    = config['ned']
    network  = config['network']
    num_devices  = config['num_devices']

    # Create directories for devices
    devices = [ f"{network}{index}" for index in range(num_devices) ]
    for device in devices:
        init_path = os.path.join(current_dir,device,'init.xml')
        with open(init_path,'w') as device_xml:
            subprocess.run(['ncs-netsim',
                            'ncs-xml-init',
                            f"{device}"],stdout=device_xml)
        subprocess.getoutput(f"echo \"config; load merge {init_path}; commit; devices device {device} sync-from\" | ncs_cli -u admin -C")
        print(f"Device {device} onboarded on NSO")
        if 'group' in config:
            subprocess.getoutput(f"echo \"config; devices device-group {config['group']} device-name {device}; commit\" | ncs_cli -u admin -C")
            print(f"Added device {device} to group {config['group']}")

@cli.command()
def remove():
    """Removes devices from NSO CDB."""
    current_dir = os.getcwd()
    config = get_config()

    # Read from config file
    ned    = config['ned']
    network  = config['network']
    num_devices  = config['num_devices']

    # Create directories for devices
    devices = [ f"{network}{index}" for index in range(num_devices) ]
    for device in devices:
        if 'group' in config:
            subprocess.getoutput(f"echo \"config; no devices device-group {config['group']} device-name {device}; commit\" | ncs_cli -u admin -C")
            print(f"Removed device {device} from group {config['group']}")

        # Don't try doing 'no devices device  ; commit' in production...
        if device != '':
            subprocess.getoutput(f"echo \"config;no devices device {device}; commit \" | ncs_cli -u admin -C")
            print(f"Removed device {device} from NSO")

@cli.command()
def save():
    """Saves current netsim devices configuration."""
    current_dir = os.getcwd()
    config = get_config()

    # Read from config file
    network  = config['network']
    num_devices  = config['num_devices']

    # Create directories for devices
    devices = [ f"{network}{index}" for index in range(num_devices) ]
    for device in devices:
        device_save = os.path.join(current_dir,device,'config.xml')
        subprocess.getoutput(f"echo \"config; show full-configuration devices device {device} | display xml \" | ncs_cli -u admin -C > {device_save}")
        print(f"Configuration for {device} saved to {device_save}")

@cli.command()
def load():
    """Load configuration for netsim devices."""
    current_dir = os.getcwd()
    config = get_config()

    # Read from config file
    network  = config['network']
    num_devices  = config['num_devices']

    # Create directories for devices
    devices = [ f"{network}{index}" for index in range(num_devices) ]
    for device in devices:
        device_save = os.path.join(current_dir,device,'config.xml')
        subprocess.getoutput(f"echo \"config; load merge {device_save}; commit\" | ncs_cli -u admin -C")
        print(f"Loaded configuration for {device} from {device_save}")

@cli.command()
def print_config():
    """Prints contents of config file""" 
    print(get_config())
    
if __name__ == '__main__':
    cli()

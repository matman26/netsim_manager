from netsim_manager.config import ManagerConfig
from netsim_manager.netsim import NetsimInfo
import ruamel.yaml as yaml
from typing import List
import subprocess
import click
import os
import re

MANAGER_FILE = 'manager.yml'

class NetsimManager():
    """
        NetsimManager stores list of Device Instances
        and handles config mgmt for running netsim
        network.
    """
    def __init__(self) -> None:
        self.current_dir = os.getcwd()
        self.config      = ManagerConfig()
        self.netsim_path = self.config.get_directory()
        self.current     = NetsimInfo(netsim_dir=self.netsim_path)
        self.network     = self.config.get_network()
        self.cfg_path    = os.path.join(self.current_dir, 'configs')

    def has_changes(self) -> bool:
        if self.current.check_exists():
            network_old = self.current.get_network()
            if self.network == network_old:
                return False
        return True

    def initialize_network(self) -> List[str]:
        if self.current.check_exists():
            raise Exception("NetsimAlreadyInitialized")

        cmds = self.network.create()
        output = []
        for cmd in cmds:
            output += os.popen(cmd)

        return output

    def update_network(self):
        if self.has_changes():
            prefixlist = self.network.prefixes
            old = self.current.get_network().prefixes
            to_add = [ prefix for prefix in prefixlist if prefix not in old ]
            print(to_add)
        else:
            print('Up to date.')

    def onboard(self):
        devices = self.network.get_devices()
        for dev in devices:
            init_path = os.path.join(self.cfg_path, dev)
            filename  = os.path.join(init_path, 'init.xml')
            os.makedirs(init_path, exist_ok=True)
            with open(filename, 'w') as device_xml:
                subprocess.run(['ncs-netsim',
                                '--dir',
                                self.netsim_path,
                                'ncs-xml-init',
                                dev],stdout=device_xml)
            output = subprocess.getoutput(f"echo \"config; load merge {filename}; commit; devices device {dev} sync-from\" | ncs_cli -u admin -C")
            print(f"Device {dev} onboarding status on NSO:")
            print(output)

    def delete(self):
        cmds = self.network.delete()
        res = []
        for cmd in cmds:
            res += os.popen(cmd)
            print(res)

    def remove(self):
        devices = self.network.get_devices()
        for device in devices:
            if device.strip() != '':
                subprocess.getoutput(f"echo \"config;no devices device {device}; commit \" | ncs_cli -u admin -C")
                print(f"Removed device {device} from NSO")

    def save(self):
        devices = self.network.get_devices()
        for device in devices:
            device_save = os.path.join(self.cfg_path, device, 'config.xml')
            subprocess.getoutput(f"echo \"config; show full-configuration devices device {device} | display xml \" | ncs_cli -u admin -C > {device_save}")
            print(f"Configuration for {device} saved to {device_save}")

    def load(self):
        devices = self.network.get_devices()
        for device in devices:
            device_save = os.path.join(self.cfg_path, device, 'config.xml')
            subprocess.getoutput(f"echo \"config; load merge {device_save}; commit\" | ncs_cli -u admin -C")
            print(f"Loaded configuration for {device} from {device_save}")

    def list_devices(self):
        net = self.current.get_network()
        print("Devices under current network:")
        for dev in net.get_devices():
            print(f'  {dev}')

    def print_settings(self):
        settings = self.config.get_settings()
        print('Configuration flags set:')
        for k, v in settings.items():
            print(f' {k}, {v}')

    def start(self):
        cmds = self.network.start()
        res = []
        for cmd in cmds:
            res += os.popen(cmd)
        print(res)

    def stop(self):
        cmds = self.network.stop()
        res = []
        for cmd in cmds:
            res += os.popen(cmd)
        print(res)

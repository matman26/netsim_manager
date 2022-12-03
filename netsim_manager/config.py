from netsim_manager.prefix import DevicePrefix
from netsim_manager.network import Network
import ruamel.yaml as yaml
from typing import List

MANAGER_FILE = 'manager.yml'
NETSIM_DIR   = '/var/netsim'

class ManagerConfig():
    """
        ManagerConfig reads config provided by the user containing mainly
        networks. Returns a list of prefixes to be configured if necessary.
    """
    def __init__(self):
        self.config    = self._get_config()
        self.directory = self.get_directory()

    def _get_config(self):
        with open(MANAGER_FILE,'r') as f:
            try:
                config = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print("Failed to read config file")
                raise exc
            return config

    def get_prefixes(self) -> List[DevicePrefix]:
        prefixes = []
        for prefix in self.config['prefixes']:
            prefixes.append(DevicePrefix(
                ned_id=prefix['ned'],
                prefix=prefix['prefix'],
                num_devices=prefix['num_devices'],
                netsim_dir=self.directory
                )
            )
        return prefixes

    def get_network(self) -> Network:
        return Network(self.get_prefixes(), self.directory)

    def get_settings(self):
        return self.config.get('settings',{})

    def get_directory(self):
        return self.get_settings().get('netsim_dir','')

from netsim_manager.prefix import DevicePrefix
from netsim_manager.network import Network
from typing import List
import os

class NetsimInfo():
    """
        NetsimInfo reads the metadata on netsim and
        provides CURRENT netsim environment config
        to compare USER-PROVIDED
    """
    def __init__(self, netsim_dir: str):
        self.netsim_dir = netsim_dir

    def check_exists(self) -> bool:
        return os.path.exists(os.path.join(self.netsim_dir, 'README.netsim'))

    def _list_to_prefixes(self, prefix_list: List) -> List[DevicePrefix]:
        prefixes = []
        for item in prefix_list:
            binary , op , opt, _dir, ned_id, num_devices, prefix = item.split()
            prefixes.append(DevicePrefix(
                ned_id=ned_id.strip(),
                prefix=prefix.strip(),
                num_devices=num_devices.strip()
                )
            )
        return prefixes

    def get_network(self) -> Network:
        lines = []
        with open(os.path.join(self.netsim_dir, 'README.netsim')) as f:
            for line in f.readlines():
                if 'create-network' in line or 'add-to-network' in line:
                    lines.append(line)

        prefixes = self._list_to_prefixes(lines)
        return Network(prefixes)

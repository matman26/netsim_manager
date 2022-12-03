from typing import List

MANAGER_FILE = 'manager.yml'

class Network():
    """
        Network represents a full netsim network containing
        potentially multiple netsim devices with multiple ned-ids
    """
    def __init__(self, prefixes, netsim_dir) -> None:
        self.prefixes   = prefixes
        self.netsim_dir = netsim_dir

    def create(self) -> List[str]:
        cmd = []
        if len(self.prefixes) > 1:
            cmd.append(self.prefixes[0].create(first=True))
            for pr in self.prefixes[1:]:
                cmd.append(pr.create(first=False))
        else:
            cmd.append(self.prefixes[0].create(first=True))
        return cmd

    def start(self) -> List[str]:
        return [ f'ncs-netsim --dir {self.netsim_dir} start' ]

    def stop(self) -> List[str]:
        return [ f'ncs-netsim --dir {self.netsim_dir} stop']

    def delete(self) -> List[str]:
        return [ f'ncs-netsim --dir {self.netsim_dir} delete-network' ]

    def get_devices(self) -> List[str]:
        devices = []
        for prefix in self.prefixes:
            devices.extend(prefix.get_devices())

        return devices
    
    def __eq__(self, other) -> bool:
        for prefix in self.prefixes:
            if prefix not in other.prefixes:
                return False
        return True

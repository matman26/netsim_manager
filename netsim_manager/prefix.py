from typing import List

class DevicePrefix():
    def __init__(self, ned_id, prefix, num_devices, netsim_dir):
        self.num_devices = num_devices
        self.ned_id      = ned_id
        self.prefix      = prefix
        self.netsim_dir  = netsim_dir

    def create(self, first: bool):
        if first:
            return f'ncs-netsim --dir {self.netsim_dir} create-network {self.ned_id} {self.num_devices} {self.prefix}'

        return f'ncs-netsim --dir {self.netsim_dir} add-to-network {self.ned_id} {self.num_devices} {self.prefix}'

    def get_devices(self) -> List[str]:
        return [ f'{self.prefix}{id}' for id in range(int(self.num_devices)) ]

    def start(self) -> List[str]:
        return [ f'ncs-netsim --dir {self.netsim_dir} start {device}' for device in self.get_devices() ]

    def stop(self) -> List[str]:
        return [ f'ncs-netsim --dir {self.netsim_dir} stop {device}'  for device in self.get_devices() ]

    def __repr__(self) -> str:
        return f'DevicePrefix: {self.prefix} {self.ned_id} {self.num_devices}'

    def __eq__(self, other):
        return ( self.num_devices, self.ned_id, self.prefix ) == (
                 other.num_devices, other.ned_id, other.prefix )

# ncs\_netsim\_manager
Declarative, config-based netsim management for reproducible, 
versionable ncs-netsim networks.

# Usage
The manager.yml file is the config file responsible for the netsim network.
A minimal yaml file looks like this:

```yaml
ned: <path-to-desired-ned-package>
network: <network-name>
num_devices: <number-of-devices>
group: <group-name> # Groups are optional
```

The `init` command creates the ncs-netsim network under the current directory. It also
creates a directory for loading and saving configs to each netsim device in the network.

```
$ ./netsim_manager.py init
DEVICE Test0 CREATED
DEVICE Test1 CREATED
```

Use `start` to start netsim instances.
```
$ ./netsim_manager.py start
DEVICE Test0 OK STARTED
DEVICE Test1 OK STARTED
```

Use `onboard` to add your devices to NSO via the CLI.
```
$ ./netsim_manager.py onboard
Device Test0 onboarded on NSO
Added device Test0 to group TEST
Device Test1 onboarded on NSO
Added device Test1 to group TEST
```

Once the device is onboarded to NSO, you are free to modify its config as you want. In
order to save the current configuration for all devices in XML format, use the
`save` command.

```
$ ./netsim_manager.py save
Configuration for Test0 saved to ./Test0/config.xml
Configuration for Test1 saved to ./Test1/config.xml
```

Saving XML configurations is very useful for creating reproducible test environments 
for larger teams, as the xml configs for netsim can be saved together with the ncs package
in order to provide an easy-to-use dev environment for specific packages. This can
even be integrated into a CI/CD pipeline!

To load configurations saved under the device's config.xml file, use the `load` command.

```
$ ./netsim_manager.py load
Loaded configuration for Test0 from ./Test0/config.xml
Loaded configuration for Test1 from ./Test1/config.xml
```

To remove the netsim devices from your NSO instance, use `remove` followed by `stop`.

``` 
$ ./netsim_manager.py remove
Removed device Test0 from group TEST
Removed device Test0 from NSO
Removed device Test1 from group TEST
Removed device Test1 from NSO
$ ./netsim_manager.py stop
DEVICE Test0 STOPPED
DEVICE Test1 STOPPED
```

# ncs\_netsim\_manager
Declarative, config-based netsim management for reproducible, 
versionable ncs-netsim networks.

# Usage
The manager.yml file is the config file responsible for the netsim network.
A minimal yaml file defines prefixes and the `netsim_dir` directory under `settings`:

```yaml
prefixes:
  - ned: /var/opt/ncs/packages/ncs-5.8.5-cisco-iosxr-7.43.4.tar.gz
    prefix: xr-
    num_devices: 2
  - ned: /var/opt/ncs/packages/ncs-5.8.5-cisco-ios-6.88.2.tar.gz
    prefix: ios-
    num_devices: 3
settings:
  netsim_dir: /var/netsim/
```

The `init` command creates the ncs-netsim network under the `netsim_dir` directory. This assumes no netsim
instances exist under the directory or onboarded on NSO. Unpredictable behavior is expected if other
netsim instances current exist.
`init` also creates a directory for loading and saving configs to each netsim device in the network.

```
$ ./netsim_manager.py init
DEVICE xr-0 CREATED
DEVICE xr-1 CREATED
DEVICE ios-0 CREATED
DEVICE ios-1 CREATED
DEVICE ios-2 CREATED
```

Use `start` to start netsim instances.
```
$ ./netsim_manager.py start
DEVICE xr-0 STARTED
DEVICE xr-1 STARTED
DEVICE ios-0 STARTED
DEVICE ios-1 STARTED
DEVICE ios-2 STARTED
```

Use `onboard` to add your devices to NSO via the CLI.
```
$ ./netsim_manager.py onboard
Device xr-0 onboarding status on NSO:
Loading.
1.43 KiB parsed in 0.00 sec (227.04 KiB/sec)
Commit complete.
result true
Device xr-1 onboarding status on NSO:
Loading.
1.43 KiB parsed in 0.00 sec (265.23 KiB/sec)
Commit complete.
result true
Device ios-0 onboarding status on NSO:
Loading.
1.43 KiB parsed in 0.00 sec (266.31 KiB/sec)
Commit complete.
result true
Device ios-1 onboarding status on NSO:
Loading.
1.43 KiB parsed in 0.00 sec (247.84 KiB/sec)
Commit complete.
result true
Device ios-2 onboarding status on NSO:
Loading.
1.43 KiB parsed in 0.00 sec (193.28 KiB/sec)
Commit complete.
result true
```

Once the device is onboarded to NSO, you are free to modify its config as you want. In
order to save the current configuration for all devices in XML format, use the
`save` command.

```
$ ./netsim_manager.py save
Configuration for xr-0 saved to /root/git/netsim_manager/configs/xr-0/config.xml
Configuration for xr-1 saved to /root/git/netsim_manager/configs/xr-1/config.xml
Configuration for ios-0 saved to /root/git/netsim_manager/configs/ios-0/config.xml
Configuration for ios-1 saved to /root/git/netsim_manager/configs/ios-1/config.xml
Configuration for ios-2 saved to /root/git/netsim_manager/configs/ios-2/config.xml
```

Saving XML configurations is very useful for creating reproducible test environments 
for larger teams, as the xml configs for netsim can be saved together with the ncs package
in order to provide an easy-to-use dev environment for specific packages. This can
even be integrated into a CI/CD pipeline!

To load configurations saved under the device's config.xml file, use the `load` command.

```
$ ./netsim_manager.py load
Loaded configuration for xr-0 from /root/git/netsim_manager/configs/xr-0/config.xml
Loaded configuration for xr-1 from /root/git/netsim_manager/configs/xr-1/config.xml
Loaded configuration for ios-0 from /root/git/netsim_manager/configs/ios-0/config.xml
Loaded configuration for ios-1 from /root/git/netsim_manager/configs/ios-1/config.xml
Loaded configuration for ios-2 from /root/git/netsim_manager/configs/ios-2/config.xml
```

To remove the netsim devices from your NSO instance, use `remove` followed by `stop`.

``` 
$ ./netsim_manager.py remove
Device xr-0: Remove OK
Commit complete.

Device xr-1: Remove OK
Commit complete.

Device ios-0: Remove OK
Commit complete.

Device ios-1: Remove OK
Commit complete.

Device ios-2: Remove OK
Commit complete.

Execution Summary:
 SUCCESS: 5
 SKIPPED: 0
 FAILED: 0
$ ./netsim_manager.py stop
DEVICE xr-0 STOPPED
DEVICE xr-1 STOPPED
DEVICE ios-0 STOPPED
DEVICE ios-1 STOPPED
DEVICE ios-2 STOPPED
```

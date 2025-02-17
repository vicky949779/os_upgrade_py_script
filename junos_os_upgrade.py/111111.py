from jnpr.junos import Device  # type: ignore
from jnpr.junos.utils.sw import SW  # type: ignore
from jnpr.junos.exception import ConnectError  # type: ignore
import getpass

# Get device credentials at runtime
host = input("Enter Junos device IP: ")
username = input("Enter username: ")
password = getpass.getpass("Enter password: ")  # Hides input for security

# Get OS file path at runtime
os_path = input("Enter OS file path on device (e.g., /var/tmp/junos-install.tgz): ")

try:
    # Connect to the Junos device
    dev = Device(host=host, user=username, passwd=password)
    dev.open()

    # Initialize Software Upgrade Utility
    sw = SW(dev)

    # Install Junos OS with automatic MD5 validation
    print("Starting Junos OS upgrade...")
    result = sw.install(package=os_path, validate=True, progress=True)

    if result is True:
        print("Upgrade successful! Rebooting device...")
        sw.reboot()
    else:
        print(f"Upgrade failed: {result}")

except ConnectError as e:
    print(f"Connection error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'dev' in locals() and dev.connected:
        dev.close()

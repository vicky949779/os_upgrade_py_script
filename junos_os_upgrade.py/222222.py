from jnpr.junos import Device  # type: ignore
from jnpr.junos.utils.sw import SW  # type: ignore
from jnpr.junos.exception import ConnectError, RpcError  # type: ignore
import getpass

# Get device credentials at runtime
host = input("Enter Junos device IP: ")
username = input("Enter username: ")
password = getpass.getpass("Enter password: ")  # Hides input for security

# OS file path on Junos device
os_path = "/var/tmp/newos.tgz"

try:
    # Connect to the Junos device
    dev = Device(host=host, user=username, passwd=password)
    dev.open()

    # Get current Junos OS version
    current_version = dev.facts.get("version")
    # print(f"Current Junos OS version: {current_version}")

    # Initialize Software Upgrade Utility
    sw = SW(dev)

    # Get the new OS version from the file
    try:
        new_version = sw.get_package_facts(os_path)["version"]
        print(f"New OS version in file: {new_version}")
    except RpcError:
        print(f"Error: OS file {os_path} not found or not valid.")
        dev.close()
        exit(1)

    # Compare OS versions
    if current_version == new_version:
        print("Device is already running the latest version. No upgrade needed.")
    else:
        print("Starting Junos OS upgrade...")
        result = sw.install(package=os_path, validate=True, progress=True)

        if result is True:
            print("Upgrade successful! Rebooting device...")
            # sw.reboot()
        else:
            print(f"Upgrade failed: {result}")

except ConnectError as e:
    print(f"Connection error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'dev' in locals() and dev.connected:
        dev.close()

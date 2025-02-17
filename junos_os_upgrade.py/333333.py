from jnpr.junos import Device # type: ignore
from jnpr.junos.utils.sw import SW # type: ignore
from jnpr.junos.exception import RpcError, ConnectError # type: ignore

host = input("Enter device IP: ")
username = input("Enter username: ")
password = input("Enter password: ")

os_path = "/var/tmp/newos.tgz"

try:
    dev = Device(host=host, user=username, passwd=password)
    dev.open()
    sw = SW(dev)

    print("Checking OS file existence...")
    try:
        new_version = sw.get_package_facts(os_path)["version"]
        print(f"New OS version: {new_version}")
    except RpcError as e:
        print(f"OS file error: {e}")
        dev.close()
        exit(1)

    print("Manually triggering installation RPC...")
    dev.rpc.request_package_add(package_name=os_path, no_validate=True)

    print("Upgrade request sent successfully. Waiting for completion...")

    # Reboot the device using RPC method
    print("Rebooting device now...")
    dev.rpc.request_reboot()

except ConnectError as e:
    print(f"Connection error: {e}")
except RpcError as e:
    print(f"RPC error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'dev' in locals() and dev.connected:
        dev.close()

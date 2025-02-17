from jnpr.junos import Device # type: ignore
from jnpr.junos.exception import ConnectError, RpcError, RpcTimeoutError # type: ignore
import time

def install_os(dev, package_path, max_retries=3, retry_delay=60):
    """
    Installs OS using request_package_add with retries on failure.
    """
    for attempt in range(1, max_retries + 1):
        try:
            print(f"\n--- Attempt {attempt}/{max_retries} ---")
            
            # Trigger OS installation
            print("Executing request_package_add RPC...")
            dev.rpc.request_package_add(
                package_name=package_path,
                no_validate=True,  # Bypass checksum validation
                dev_timeout=1800   # 30-minute timeout
            )
            print("OS installation triggered successfully.")
            return True  # Success

        except RpcTimeoutError as e:
            print(f"Timeout error: {e}")
            if attempt < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Installation failed.")
                return False  # Failure

def main():
    host = input("Enter device IP: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    os_path = "/var/tmp/newos.tgz"  # Ensure this file exists on the device

    dev = None
    try:
        # Connect to the device
        dev = Device(host=host, user=username, passwd=password, timeout=1800)
        dev.open()
        print(f"Connected to {dev.facts['hostname']}")

        # Install OS
        if not install_os(dev, os_path):
            exit(1)

        # Reboot the device
        print("\nRebooting device now...")
        dev.rpc.request_reboot()
        print("Reboot command sent. Wait 5-10 minutes before reconnecting.")

    except (ConnectError, RpcError, RpcTimeoutError) as e:
        print(f"\nFatal error: {e}")
        exit(1)
    finally:
        if dev and dev.connected:
            dev.close()

if __name__ == "__main__":
    main()

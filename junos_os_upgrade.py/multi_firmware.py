from jnpr.junos import Device # type: ignore
from jnpr.junos.utils.sw import SW # type: ignore
import subprocess
import time

def is_device_reachable(hostname):
    """Ping the device to check if it's reachable."""
    response = subprocess.run(['ping', '-c', '1', '-W', '3', hostname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return response.returncode == 0

def upgrade_firmware(hostname, username, password, firmware_list):
    """Upgrades the OS sequentially from the provided firmware list using PyEZ."""
    firmware_versions = firmware_list.split(',')  # Split multiple firmware inputs
    
    try:
        with Device(host=hostname, user=username, passwd=password) as dev:
            sw = SW(dev)
            
            for index, firmware in enumerate(firmware_versions):
                firmware = firmware.strip()
                print(f"\U0001F680 Starting upgrade to: {firmware}")
                
                try:
                    # Install firmware
                    sw.install(package=firmware, validate=True, progress=True)
                    print(f"\U00002705 Upgrade to {firmware} completed! Rebooting...")
                    
                    # Reboot device
                    sw.reboot()
                    print("\U0001F4BB Waiting for device to come online...")
                    
                    # Wait and check reachability
                    time.sleep(60)  # Wait before checking
                    if is_device_reachable(hostname):
                        print(f"\U0001F4BB Device reachable after {firmware} upgrade. Proceeding...")
                    else:
                        print(f"\U0000274C Device unreachable after {firmware} upgrade. Stopping further upgrades.")
                        return
                except Exception as err:
                    print(f"\U0000274C Error during {firmware} upgrade: {err}")
                    return
    
        print("\U0001F389 All OS upgrades completed successfully!")
    except Exception as e:
        print(f"\U0000274C Connection failed: {e}")

# Example usage
hostname = input("Enter device IP/Hostname: ")
username = input("Enter username: ")
password = input("Enter password: ")
firmware_input = input("Enter firmware versions (comma-separated): ")
upgrade_firmware(hostname, username, password, firmware_input)

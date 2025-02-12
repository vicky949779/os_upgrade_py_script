# from jnpr.junos import Device # type: ignore
# from jnpr.junos.exception import ConnectError # type: ignore

# def show_version(host, username, password):
#     """
#     Connects to a Junos device via SSH and runs the 'show version' command.
#     """
#     dev = Device(host=host, user=username, passwd=password)

#     try:
#         print(f"🔌 Connecting to {host}...")
#         dev.open()
#         print("✅ Connection successful!\n")

#         # Execute 'show version' command
#         print("📢 Running 'show version' command...")
#         output = dev.cli('show version')
#         print(output)

#     except ConnectError as err:
#         print(f"❌ Connection failed: {err}")
#     except Exception as err:
#         print(f"❌ Unexpected error: {err}")
#     finally:
#         if dev.connected:
#             dev.close()
#             print("🔌 Connection closed.")

# # Example usage
# show_version(host='192.168.40.10', username='admin', password='Abcd@123')
from jnpr.junos import Device  # type: ignore
from jnpr.junos.exception import ConnectError  # type: ignore
from lxml import etree  # Required for XML parsing
import getpass  # For secure password input

def os_upgrade():
    """
    Connects to a Junos device via SSH and retrieves software version using RPC.
    """
    host = input("🔹 Enter device IP/Hostname: ")
    username = input("🔹 Enter username: ")
    password = getpass.getpass("🔹 Enter password: ")  # Secure password input

    dev = Device(host=host, user=username, passwd=password)

    try:
        print(f"\n🔌 Connecting to {host}...")
        dev.open()
        print("✅ Connection successful!\n")

        # Recommended method: Using RPC to get software version
        print("📢 Fetching software information using RPC...\n")
        sw_info = dev.rpc.get_software_information()

        # Pretty-print the XML output
        print(etree.tostring(sw_info, pretty_print=True).decode())

    except ConnectError as err:
        print(f"❌ Connection failed: {err}")
    except Exception as err:
        print(f"❌ Unexpected error: {err}")
    finally:
        if dev.connected:
            dev.close()
            print("\n🔌 Connection closed.")

# Run the function
os_upgrade()


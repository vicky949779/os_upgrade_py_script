# from jnpr.junos import Device  # type: ignore
# from jnpr.junos.exception import ConnectError  # type: ignore
# from lxml import etree  # type: ignore # Required for XML parsing
# import getpass  # For secure password input

# def execute_rpc_commands(dev, commands):
#     """
#     Executes a list of Junos RPC or CLI commands and prints the output.
#     """
#     for cmd in commands:
#         try:
#             print(f"\n🔹 Executing: {cmd['description']}")
            
#             if cmd['method'] == 'cli':
#                 output = dev.cli(cmd['args']['command'])
#             else:
#                 rpc_method = getattr(dev.rpc, cmd['method'])
#                 output = rpc_method(**cmd.get('args', {}))
#                 output = etree.tostring(output, pretty_print=True).decode()
            
#             print(output)

#         except Exception as err:
#             print(f"❌ Error executing '{cmd['description']}': {err}")

# def os_upgrade():
#     """
#     Connects to a Junos device via SSH, runs pre-check commands,
#     and retrieves software version using RPC.
#     """
#     host = input("🔹 Enter device IP/Hostname: ")
#     username = input("🔹 Enter username: ")
#     password = getpass.getpass("🔹 Enter password: ")  # Secure password input

#     # Define RPC and CLI commands to execute
#     rpc_commands = [
#         {
#             'description': 'Show version',
#             'method': 'get_software_information',
#             'args': { 'format': 'text'}
#             # 'cli_fallback': 'show version'
#         },
#         {
#             'description': 'Show interfaces terse',
#             'method': 'get_interface_information',
#             'args': {'terse': True,'format': 'text' },
#             # 'cli_fallback': 'show interfaces terse'
#         },
#         {
#             'description': 'Show LLDP neighbors',
#             'method': 'get_lldp_neighbors_information',
#             # 'cli_fallback': 'show lldp neighbors'
#             'args': { 'format': 'text'}
#         },
#         {
#             'description': 'Show virtual-chassis',
#             'method': 'get_virtual_chassis_information',
#             # 'cli_fallback': 'show virtual-chassis',
#             'args': { 'format': 'text'}
#         },
#         {
#             'description': 'Show interfaces description',
#             'method': 'cli',
#             'args': {'command': 'show configuration interfaces | match description','format': 'text'},
#             # 'cli_fallback': 'show configuration interfaces | match description'
#         }
#     ]

#     # Use 'with' to manage device connection automatically
#     try:
#         with Device(host=host, user=username, passwd=password) as dev:
#             print(f"\n🔌 Connecting to {host}...")
#             print("✅ Connection successful!\n")

#             # Run pre-check RPC commands
#             print("📢 Running pre-check commands...")
#             execute_rpc_commands(dev, rpc_commands)

#     except ConnectError as err:
#         print(f"❌ Connection failed: {err}")
#     except Exception as err:
#         print(f"❌ Unexpected error: {err}")

# # Run the function
# os_upgrade()

#############################################################################
""" comparision command """

from jnpr.junos import Device  # type: ignore
from jnpr.junos.exception import ConnectError, RpcError  # type: ignore
from lxml import etree  # type: ignore
import getpass  # Secure password input
import os
import difflib
from tabulate import tabulate # type: ignore

# Output file names
PRECHECK_OUTPUT_FILE = "ppp.txt"
POSTCHECK_OUTPUT_FILE = "precheck_outputs.txt"

def get_current_directory():
    """Returns the current working directory."""
    cwd = os.getcwd()
    print(f"\U0001F4C2 Current Directory: {cwd}")
    return cwd

def compare_files(precheck_data, postcheck_data):
    """Compares two file contents and returns old (-) and new (+) changes."""
    diff = list(difflib.ndiff(precheck_data, postcheck_data))

    old_changes = [line[2:].strip() for line in diff if line.startswith("- ")]  # Removed
    new_changes = [line[2:].strip() for line in diff if line.startswith("+ ")]  # Added

    return old_changes, new_changes

def format_and_print_table(old_changes, new_changes):
    """Formats and prints the differences in table format."""
    max_len = max(len(old_changes), len(new_changes))

    # Ensure both lists have equal length
    old_changes.extend([""] * (max_len - len(old_changes)))
    new_changes.extend([""] * (max_len - len(new_changes)))

    changes = list(zip(new_changes, old_changes))

    if any(new_changes) or any(old_changes):
        print("\n\U0000274C Changes detected! Showing differences...\n")
        table_headers = ["New Changes (+)", "Old Changes (-)"]
        print(tabulate(changes, headers=table_headers, tablefmt="grid"))
    else:
        print("\n\U00002705 No differences found between precheck and postcheck outputs.")

def read_file(filepath):
    """Reads the content of a file and returns it as a list of lines."""
    try:
        with open(filepath, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"\U0000274C Error: File not found -> {filepath}")
        return []

def os_upgrade():
    """
    Connects to a Junos device via SSH, runs pre-check commands, 
    performs the upgrade (placeholder), and then runs post-check commands.
    """
    host = input("🔹 Enter device IP/Hostname: ")
    username = input("🔹 Enter username: ")
    password = getpass.getpass("🔹 Enter password: ")  # Secure password input


    try:
        with Device(host=host, user=username, passwd=password) as dev:
            print(f"\n🔌 Connecting to {host}...")
            print("✅ Connection successful!\n")

            # Run Comparision 
            cwd = get_current_directory()
            # Define file paths
            precheck_file = os.path.join(cwd, "ppp.txt")
            postcheck_file = os.path.join(cwd, "precheck_outputs.txt")
            # Read file contents
            precheck_data = read_file(precheck_file)
            postcheck_data = read_file(postcheck_file)

            if not precheck_data or not postcheck_data:
                print("\U0000274C Comparison failed due to missing files.")
                return
            # Compare files and get changes
            old_changes, new_changes = compare_files(precheck_data, postcheck_data)
            # Print formatted table
            format_and_print_table(old_changes, new_changes)

    except ConnectError as err:
        print(f"❌ Connection failed: {err}")
    except Exception as err:
        print(f"❌ Unexpected error: {err}")

# Run the function
os_upgrade()

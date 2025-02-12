from jnpr.junos import Device  # type: ignore
from jnpr.junos.exception import ConnectError, RpcError  # type: ignore
from lxml import etree  # type: ignore
import getpass  # Secure password input
import os
import difflib
from tabulate import tabulate # type: ignore

def get_current_directory():
    """Returns the current working directory."""
    cwd = os.getcwd()
    print(f"\U0001F4C2 Current Directory: {cwd}")
    return cwd

def read_file(filepath):
    """Reads the content of a file and returns it as a list of lines."""
    try:
        with open(filepath, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"\U0000274C Error: File not found -> {filepath}")
        return []

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

def run_checks(dev, commands, phase):
    """
    Executes CLI and RPC commands and saves the exact Junos output to a text file.
    """
    # Output file names
    PRECHECK_OUTPUT_FILE = "precheck_outputs.xml"
    POSTCHECK_OUTPUT_FILE = "postcheck_outputs.xml"
    output_file = PRECHECK_OUTPUT_FILE if phase == "pre-check" else POSTCHECK_OUTPUT_FILE

    with open(output_file, "w") as file:  # Overwrites file for each run
        for cmd in commands:
            try:
                print(f"\n\U0001F539 Executing {phase}: {cmd['description']}")

                if cmd['method'] == 'cli':
                    output = dev.cli(cmd['args']['command'])  # CLI output as-is
                else:
                    rpc_method = getattr(dev.rpc, cmd['method'])
                    response = rpc_method(**cmd.get('args', {}))
                    output = etree.tostring(response, pretty_print=True, encoding="unicode")  # Ensure formatted XML output  

                # Write output exactly as it appears on Junos device
                file.write(f"\n===== {cmd['description']}  =====\n")
                file.write(output + "\n")

                print(output)  # Print the exact same output

            except RpcError as rpc_err:
                print(f"\U0000274C RPC Error executing '{cmd['description']}': {rpc_err}")
            except Exception as err:
                print(f"\U0000274C Error executing '{cmd['description']}': {err}")

    print(f"\n\U0001F4C4 Successfully executed {phase} results saved in '{output_file}'")

def os_upgrade():
    """
    Connects to a Junos device via SSH, runs pre-check commands, 
    performs the upgrade (placeholder), and then runs post-check commands.
    """
    host = input("\U0001F539 Enter device IP/Hostname: ")
    username = input("\U0001F539 Enter username: ")
    password = getpass.getpass("\U0001F539 Enter password: ")  # Secure password input

    # Define CLI & RPC commands
    commands = [
        {'description': 'Show version', 'method': 'get_software_information'},
        {'description': 'Show interfaces terse', 'method': 'get_interface_information', 'args': {'terse': True}},
        {'description': 'Show LLDP neighbors', 'method': 'get_lldp_neighbors_information'},
        {'description': 'Show virtual-chassis', 'method': 'get_virtual_chassis_information'},
        {'description': 'Show interfaces description', 'method': 'get_interface_information', 'args': {'descriptions': True}},
        {'description': 'Show Ethernet Switching Table', 'method': 'get_ethernet_switching_table_information'}
    ]
    try:
        with Device(host=host, user=username, passwd=password) as dev:
            print(f"\n🔌 Connecting to {host}...")
            print("\U00002705 Connection successful!\n")

            # Run pre-checks
            print("\U0001F4E2 Running PRE-CHECK commands...")
            run_checks(dev, commands, phase="pre-check")

            # Placeholder for upgrade process
            print("\n\U0001F680 Performing OS upgrade... (Add actual upgrade logic here)")
            # Add upgrade logic here

            # Run post-checks
            print("\n\U0001F4E2 Running POST-CHECK commands...")
            run_checks(dev, commands, phase="post-check")

            # Run Comparision 
            cwd = get_current_directory()
            # Define file paths
            precheck_file = os.path.join(cwd, "precheck_outputs.xml")
            postcheck_file = os.path.join(cwd, "postcheck_outputs.xml")
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
        print(f"\U0000274C Connection failed: {err}")
    except Exception as err:
        print(f"\U0000274C Unexpected error: {err}")

os_upgrade()



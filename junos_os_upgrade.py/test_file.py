# from jnpr.junos import Device  # type: ignore
# from jnpr.junos.exception import ConnectError  # type: ignore
# from lxml import etree  # type: ignore  # Required for XML parsing
# import getpass  # For secure password input
# from jnpr.junos.utils.start_shell import StartShell  # type: ignore
# from pprint import pprint

# host = input("🔹 Enter device IP/Hostname: ")
# username = input("🔹 Enter username: ")
# password = getpass.getpass("🔹 Enter password: ")  # Secure password input

# rpc_commands = [
#     "show ethernet-switching table",
#     "show version",
#     "show interfaces terse",
#     "show interfaces descriptions",
#     "show lldp neighbors",
#     "show virtual-chassis"
# ]

# def execute_commands(ss, commands):
#     """
#     Executes a list of Junos CLI commands using 'cli -c' and prints the output.
#     """
#     for cmd in commands:
#         try:
#             print(f"\n🔹 Executing: {cmd}")
#             command = f'cli -c "{cmd}"'
#             output_code, output_text = ss.run(command, this=None, timeout=15)  # Fix output format
#             pprint(output_text)  # Print only actual command output
#         except Exception as err:
#             print(f"❌ Error executing '{cmd}': {err}")

# def os_upgrade():
#     """
#     Connects to a Junos device via SSH, runs pre-check commands,
#     and retrieves software version using StartShell.
#     """
#     dev = Device(host=host, user=username, passwd=password)

#     # Use 'with' to manage device connection automatically
#     try:
#         with StartShell(dev) as ss:
#             print(f"\n🔌 Connecting to {host}...")
#             print("✅ Connection successful!\n")

#             # Run pre-check CLI commands
#             print("📢 Running pre-check commands...")
#             execute_commands(ss, rpc_commands)

#     except ConnectError as err:
#         print(f"❌ Connection failed: {err}")
#     except Exception as err:
#         print(f"❌ Unexpected error: {err}")

# # Run the function
# os_upgrade()


from jnpr.junos import Device  # type: ignore
from jnpr.junos.exception import ConnectError, RpcError  # type: ignore
from lxml import etree  # type: ignore
import getpass  # Secure password input

OUTPUT_FILE = "precheck_outputs.txt"  # Define output file name

def execute_commands(dev, commands):
    """
    Executes a list of Junos RPC or CLI commands and stores only successful output in a text file.
    """
    with open(OUTPUT_FILE, "w") as file:  # Open file in write mode
        for cmd in commands:
            try:
                print(f"\n🔹 Executing: {cmd['description']}")

                if cmd['method'] == 'cli':
                    output = dev.cli(cmd['args']['command'])
                else:
                    rpc_method = getattr(dev.rpc, cmd['method'])
                    response = rpc_method(**cmd.get('args', {}))

                    # # Convert XML output to text
                    if isinstance(response, etree._Element):
                        output = etree.tostring(response, pretty_print=True).decode()
                    else:
                        output = str(response)  # Ensure response is stored as text
                    
               
                # Store only successful outputs in the file
                file.write(f"\n===== {cmd['description']} =====\n")
                file.write(output + "\n")
                
                print(output)  # Print output to console

            except RpcError as rpc_err:
                print(f"❌ RPC Error executing '{cmd['description']}': {rpc_err}")
            except Exception as err:
                print(f"❌ Error executing '{cmd['description']}': {err}")

    print(f"\n📄 Successfully executed command results saved in '{OUTPUT_FILE}'")

def os_upgrade():
    """
    Connects to a Junos device via SSH, runs pre-check commands,
    and retrieves software version using RPC.
    """
    host = input("🔹 Enter device IP/Hostname: ")
    username = input("🔹 Enter username: ")
    password = getpass.getpass("🔹 Enter password: ")  # Secure password input

    # Define RPC and CLI commands to execute
    commands = [
        {'description': 'Show version', 'method': 'get_software_information'},
        {'description': 'Show interfaces terse', 'method': 'get_interface_information', 'args': {'terse': True}},
        {'description': 'Show LLDP neighbors', 'method': 'get_lldp_neighbors_information'},
        {'description': 'Show virtual-chassis', 'method': 'get_virtual_chassis_information'},
        {'description': 'Show interfaces description', 'method': 'cli', 'args': {'command': 'show configuration interfaces | match description'}},
        {'description': 'Show Ethernet Switching Table','method': 'get_ethernet_switching_table_information'}
    ]

    try:
        with Device(host=host, user=username, passwd=password) as dev:
            print(f"\n🔌 Connecting to {host}...")
            print("✅ Connection successful!\n")

            # Run commands and store only successful outputs in a file
            print("📢 Running pre-check commands...")
            execute_commands(dev, commands)

    except ConnectError as err:
        print(f"❌ Connection failed: {err}")
    except Exception as err:
        print(f"❌ Unexpected error: {err}")

# Run the function
os_upgrade()

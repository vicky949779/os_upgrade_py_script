# from jnpr.junos import Device  # type: ignore
# from jnpr.junos.exception import ConnectError, RpcError  # type: ignore
# from lxml import etree  # type: ignore
# import getpass  # Secure password input

# def run_checks(dev, commands, phase):
#     """
#     Executes CLI and RPC commands and saves the exact Junos output to a text file.
#     """
#     # Output file names
#     PRECHECK_OUTPUT_FILE = "precheck_outputs.txt"
#     POSTCHECK_OUTPUT_FILE = "postcheck_outputs.txt"
#     output_file = PRECHECK_OUTPUT_FILE if phase == "pre-check" else POSTCHECK_OUTPUT_FILE

#     with open(output_file, "w") as file:  # Overwrites file for each run
#         for cmd in commands:
#             try:
#                 print(f"\n🔹 Executing {phase}: {cmd['description']}")

#                 if cmd['method'] == 'cli':
#                     output = dev.cli(cmd['args']['command'])  # CLI output as-is
#                 else:
#                     rpc_method = getattr(dev.rpc, cmd['method'])
#                     response = rpc_method(**cmd.get('args', {}))
#                     output = etree.tostring(response, pretty_print=True, encoding="unicode")  # Ensure formatted XML output  

#                 # Write output exactly as it appears on Junos device
#                 file.write(f"\n===== {cmd['description']}  =====\n")
#                 file.write(output + "\n")

#                 print(output)  # Print the exact same output

#             except RpcError as rpc_err:
#                 print(f"❌ RPC Error executing '{cmd['description']}': {rpc_err}")
#             except Exception as err:
#                 print(f"❌ Error executing '{cmd['description']}': {err}")

#     print(f"\n📄 Successfully executed {phase} results saved in '{output_file}'")

# def os_upgrade():
#     """
#     runs pre-check commands, 
#     """
#     # Define CLI & RPC commands
#     commands = [
#         {'description': 'Show version', 'method': 'get_software_information'},
#         {'description': 'Show interfaces terse', 'method': 'get_interface_information', 'args': {'terse': True}},
#         {'description': 'Show LLDP neighbors', 'method': 'get_lldp_neighbors_information'},
#         {'description': 'Show virtual-chassis', 'method': 'get_virtual_chassis_information'},
#         {'description': 'Show interfaces description', 'method': 'get_interface_information', 'args': {'descriptions': True}},
#         {'description': 'Show Ethernet Switching Table', 'method': 'get_ethernet_switching_table_information'}
#     ]

#     print(f"\n🔌 Connecting to {host}...")
#     print("✅ Connection successful!\n")

#     # Run pre-checks
#     print("📢 Running PRE-CHECK commands...")
#     run_checks(dev, commands, phase="pre-check")
                    
# # Run the function
# os_upgrade()

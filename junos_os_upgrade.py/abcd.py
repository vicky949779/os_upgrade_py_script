import getpass
import time
import warnings
from jnpr.junos import Device # type: ignore
from jnpr.junos.exception import ConnectError # type: ignore
from jnpr.junos.op.phyport import PhyPortTable  # For interface details # type: ignore
from lxml import etree  # For XML parsing # type: ignore
 
# Suppress RuntimeWarnings from PyEZ
# warnings.simplefilter('ignore', RuntimeWarning)
 
def establish_ssh_connection(hostname, username, password):
    """Establish a connection to the Juniper device using PyEZ."""
    try:
        print(f"Connecting to {hostname}...")
        dev = Device(host=hostname, user=username, passwd=password)
        dev.open()
        print(f"Connected to {hostname}.")
        return dev
    except ConnectError as e:
        print(f"Failed to connect to {hostname}: {e}")
        return None
 
def extract_text_from_xml(xml_element):
    """Extracts relevant information from an XML element and formats it as readable text."""
    if isinstance(xml_element, bool):  # ✅ Handle boolean responses
        return "Success" if xml_element else "Failed"
 
    output = []
    for element in xml_element.iter():
        if element.tag is not None and element.text is not None:
            tag = element.tag.replace("-", " ").strip()  # Replace hyphens for readability
            text = element.text.strip()
            if text:
                output.append(f"{tag}: {text}")
 
    return "\n".join(output)
 
def execute_command(dev, cmd):
    """Execute RPC or CLI commands and return human-readable text output."""
    try:
        if cmd['method'] == 'cli':
            rpc_output = dev.cli(cmd['args']['command'])  # CLI commands return strings
        else:
            rpc_method = getattr(dev.rpc, cmd['method'])
            rpc_output = rpc_method(**cmd.get('args', {}))  # RPC methods return XML
 
        # ✅ Handle string responses (CLI) separately
        if isinstance(rpc_output, str):
            return rpc_output.strip(), None
 
        # ✅ Handle XML responses properly
        formatted_output = extract_text_from_xml(rpc_output)
        return formatted_output, None
 
    except Exception as e:
        return None, str(e)
 
def save_output_to_file(filename, output):
    """Save command output to a file."""
    with open(filename, 'w') as file:
        file.write(output)
 
def main():
    #username = input("Enter your username: ")
    #password = getpass.getpass("Enter your password: ")
    #target_device = input("Enter switch hostname: ")
 
    dev = establish_ssh_connection("192.168.40.151","admin","Abcd@123")
    if not dev:
        return
 
    pre_check_commands = [
        {'description': 'Show version', 'method': 'get_software_information'},
        {'description': 'Show interfaces terse', 'method': 'get_interface_information', 'args': {'terse': True}},
        {'description': 'Show LLDP neighbors', 'method': 'get_lldp_neighbors_information'},
        {'description': 'Show virtual-chassis', 'method': 'get_virtual_chassis_information'},
        {'description': 'Show interfaces description', 'method': 'cli', 'args': {'command': 'show configuration interfaces | match description'}},
        {'description': 'Show Ethernet Switching Table','method': 'get_ethernet_switching_table_information'}
    ]
    pre_check_output = ""
    for command in pre_check_commands:
        output, error = execute_command(dev, command)
        if error:
            print(f"Error executing {command}: {error}")
        else:
            pre_check_output += f"Command: {command}\n{output}\n{'-'*50}\n"
 
    save_output_to_file("pre.txt", pre_check_output)
    print("Pre-checks completed without warnings.")
 
if __name__ == "__main__":
    main()
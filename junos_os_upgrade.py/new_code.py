import getpass
import re
import time
from jnpr.junos import Device
from jnpr.junos.utils.scp import SCP
from jnpr.junos.utils.fs import FS
from jnpr.junos.utils.sw import SW
from jnpr.junos.exception import ConnectError

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

def execute_command(dev, command):
    """Execute a CLI command on the device and return output."""
    try:
        output = dev.cli(command, format="text")
        return output, None
    except Exception as e:
        return None, str(e)

def parse_interfaces_descriptions(output, regex_pattern):
    """Parse 'show interfaces descriptions' to find all links and their statuses."""
    interfaces = {}
    lines = output.splitlines()
    for line in lines[1:]:  # Skip header line
        parts = line.split()
        interface = parts[0]
        admin_status = parts[1].lower() if len(parts) > 1 and parts[1] else ""
        link_status = parts[2].lower() if len(parts) > 2 and parts[2] else ""
        description = parts[-1] if parts else ""
        is_uplink = re.search(regex_pattern, description) is not None
        interfaces[interface] = {
                "admin_up": admin_status == "up",
                "link_up": link_status == "up",
                "is_uplink": is_uplink,
                "description": description
            }
    return interfaces

def save_output_to_file(filename, output):
    """Save command output to a file."""
    with open(filename, 'w') as file:
        file.write(output)

def copy_firmware(dev, firmware_path, destination):
    """Copy firmware to the device using PyEZ FileSystem."""
    try:    
        print(f"Checking if {firmware_path} exists on the target device...")
        output, error = execute_command(dev, f"file list /var/tmp/{firmware_path}")
        if "No such file" in output:
            print(f"{firmware_path} not found on the target device. Copying it from the corpjump server...")
            with SCP(dev, progress=True) as scp:
                scp.put(firmware_path, destination)
            print(f"Firmware {firmware_path} copied to {destination}.")
        else:
            print(f"{firmware_path} already exists on the target device.")
    except Exception as e:
        print(f"Failed to copy firmware: {e}")

def validate_firmware(dev, firmware, expected_md5):
    """Validate the firmware MD5 checksum."""
    fs = FS(dev)
        # Get MD5 checksum
    output = fs.checksum(firmware, algorithm='md5')    
    match = re.search(r'[a-fA-F0-9]{32}', output)
    if match:
        device_md5 = match.group(0)
        if device_md5 != expected_md5:
            print(f"MD5 mismatch! Expected: {expected_md5}, Found: {device_md5}")
            return False
        print("MD5 checksum verified.")
        return True
    print("Could not retrieve MD5 checksum.")
    return False

def upgrade_firmware(dev, firmware_path):
    """Upgrade JunOS firmware using PyEZ SW module."""
    try:
        sw = SW(dev)
        print("Starting firmware upgrade...")
        success = sw.install(package=firmware_path, progress=True, validate=True)
        if success:
            print("Firmware upgrade completed successfully. Rebooting device...")
            dev.reboot()
        else:
            print("Firmware upgrade failed.")
    except Exception as e:
        print(f"Upgrade error: {e}")

def is_device_reachable(hostname):
    """Ping the device to check if it's reachable."""
    import subprocess
    response = subprocess.run(['ping', '-c', '1', '-W', '3', hostname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return response.returncode == 0

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
def compare_files(pre_data, post_data):
    """Compare pre-check and post-check data."""
    changes = []
    max_lines = max(len(pre_data), len(post_data))

    for i in range(max_lines):
        pre_line = pre_data[i] if i < len(pre_data) else ""
        post_line = post_data[i] if i < len(post_data) else ""
        
        if pre_line != post_line:
            changes.append((pre_line, post_line))
    
    return changes

def extract_info(file_content):
    """Extract all relevant information from the file content."""
    return file_content.splitlines()

def wrap_text(text, width):
    """Wrap text to fit within a specified width."""
    lines = []
    while len(text) > width:
        # Find the last space within the width
        split_index = text[:width].rfind(" ")
        if split_index == -1:  # No spaces found, split at width
            split_index = width
        lines.append(text[:split_index].strip())
        text = text[split_index:].strip()
    lines.append(text)  # Add the remaining text
    return lines

def save_table_to_file(changes, output_file):
    """Save changes in a table format to a file with text wrapping."""
    col_width = 50
    table_width = 2 * col_width + 7  # Includes borders and separator

    with open(output_file, "w") as f:
        # Write top border
        f.write("+" + "-" * (table_width - 2) + "+\n")

        # Write header row
        header = f"| {'Pre-Check':<{col_width}} | {'Post-Check':<{col_width}} |\n"
        f.write(header)
        f.write("+" + "-" * (table_width - 2) + "+\n")

        # Write data rows with text wrapping
        for pre, post in changes:
            pre_lines = wrap_text(pre, col_width)
            post_lines = wrap_text(post, col_width)
            max_lines = max(len(pre_lines), len(post_lines))

            for i in range(max_lines):
                pre_line = pre_lines[i] if i < len(pre_lines) else ""
                post_line = post_lines[i] if i < len(post_lines) else ""
                f.write(f"| {pre_line:<{col_width}} | {post_line:<{col_width}} |\n")

        # Write bottom border
        f.write("+" + "-" * (table_width - 2) + "+\n")

    print(f"Comparison saved to {output_file}")


def main():
    
    pre_check_output = """
Command: show ethernet-switching table

--------------------------------------------------
Command: show version
fpc0:
--------------------------------------------------------------------------
Hostname: vqfx-release
Model: vqfx-10000
Junos: 18.1R1.9 limited
JUNOS Base OS boot [18.1R1.9]
JUNOS Base OS Software Suite [18.1R1.9]
JUNOS Crypto Software Suite [18.1R1.9]
JUNOS Online Documentation [18.1R1.9]
JUNOS Kernel Software Suite [18.1R1.9]
JUNOS Packet Forwarding Engine Support (qfx-10-f) [18.1R1.9]
JUNOS Routing Software Suite [18.1R1.9]
JUNOS jsd [i386-18.1R1.9-jet-1]
JUNOS SDN Software Suite [18.1R1.9]
JUNOS Enterprise Software Suite [18.1R1.9]
JUNOS Web Management [18.1R1.9]
JUNOS py-base-i386 [18.1R1.9]
JUNOS py-extensions-i386 [18.1R1.9]

--------------------------------------------------
Command: show interfaces terse
Interface               Admin Link Proto    Local                 Remote
gr-0/0/0                up    up
bme0                    up    up
bme0.0                  up    up   inet     128.0.0.1/2     
                                            128.0.0.4/2     
                                            128.0.0.16/2    
                                            128.0.0.63/2    
cbp0                    up    up
dsc                     up    up
em0                     up    up
em0.0                   up    up   inet     192.168.40.131/24
em1                     up    up
em1.0                   up    down inet     169.254.0.2/24  
em2                     up    down
em2.32768               up    down inet     192.168.1.2/24  
em3                     up    down
em4                     up    down
em4.32768               up    down inet     192.0.2.2/24    
em5                     up    down
em6                     up    down
em7                     up    up
em8                     up    down
em9                     up    down
em10                    up    down
em11                    up    down
esi                     up    up
gre                     up    up
ipip                    up    up
irb                     up    up
jsrv                    up    up
jsrv.1                  up    up   inet     128.0.0.127/2   
lo0                     up    up
lo0.0                   up    up   inet    
                                   inet6    fe80::205:860f:fc71:f700
lo0.16385               up    up   inet    
lsi                     up    up
mtun                    up    up
pimd                    up    up
pime                    up    up
pip0                    up    up
tap                     up    up
vme                     up    down
vtep                    up    up

--------------------------------------------------
Command: show interfaces descriptions
Interface       Admin Link Description
em0             up    up   Management Interface
em1             up    down Uplink to Core Switch
em2             up    down Backup Link
em3             up    down Customer VLAN
em4             up    down Server Network
em5             up    down Unused Interface
em6             up    down WAN Connection

--------------------------------------------------
Command: show lldp neighbors

--------------------------------------------------
Command: show virtual-chassis

Virtual Chassis ID: 6c89.751e.e97c
Virtual Chassis Mode: Enabled
                                                Mstr           Mixed Route Neighbor List
Member ID  Status   Serial No    Model          prio  Role      Mode  Mode ID  Interface
0 (FPC 0)  Prsnt    817789208176 vqfx-10000     128   Master*      N  VC

Member ID for next new member: 1 (FPC 1)

--------------------------------------------------


"""
    post_check_output = """
Command: show ethernet-switching table

--------------------------------------------------
Command: show version
fpc0:
--------------------------------------------------------------------------
Hostname: vqfx-re
Model: vqfx-10000
Junos: 18.1R1.91 limited
JUNOS Base OS boot [18.1R1.9]
JUNOS Base OS Software Suite [18.1R1.9]
JUNOS Crypto Software Suite [18.1R1.9]
JUNOS Online Documentation [18.1R1.9]
JUNOS Kernel Software Suite [18.1R1.9]
JUNOS Packet Forwarding Engine Support (qfx-10-f) [18.1R1.9]
JUNOS Routing Software Suite [18.1R1.9]
JUNOS jsd [i386-18.1R1.9-jet-1]
JUNOS SDN Software Suite [18.1R1.9]
JUNOS Enterprise Software Suite [18.1R1.9]
JUNOS Web Management [18.1R1.9]
JUNOS py-base-i386 [18.1R1.9]
JUNOS py-extensions-i386 [18.11R1.9]

--------------------------------------------------
Command: show interfaces terse
Interface               Admin Link Proto    Local                 Remote
gr-0/0/0                down    up
bme0                    up    up
bme0.0                  up    up   inet     128.0.0.1/2     
                                            128.0.0.4/2     
                                            128.0.0.16/2    
                                            128.0.0.63/2    
cbp0                    up    up
dsc                     up    up
em0                     up    up
em0.0                   up    up   inet     191.168.40.131/24
em1                     up    down
em1.0                   up    down inet     169.254.0.2/24  
em2                     up    down
em2.32768               up    down inet     192.168.1.2/24  
em3                     up    down
em4                     up    down
em4.32768               up    down inet     192.0.2.2/24    
em5                     up    down
em6                     up    down
em7                     up    down
em8                     up    down
em9                     up    down
em10                    up    down
em11                    up    down
esi                     up    up
gre                     up    up
ipip                    up    up
irb                     up    up
jsrv                    up    up
jsrv.1                  up    up   inet     128.0.0.127/2   
lo0                     up    up
lo0.0                   up    up   inet    
                                   inet6    fe80::205:860f:fc71:f700
lo0.16385               up    up   inet    
lsi                     up    up
mtun                    up    up
pimd                    up    up
pime                    up    up
pip0                    up    up
tap                     up    up
vme                     up    down
vtep                    up    up

--------------------------------------------------
Command: show interfaces descriptions
Interface       Admin Link Description
em0             up    up   Management Interface
em1             down    down Uplink to Core Switch
em2             down    down Backup Link
em3             up    down Customer VLAN
em4             up    down Server Network
em5             up    down Unused Interface
em6             up    down WAN Connection

--------------------------------------------------
Command: show lldp neighbors

--------------------------------------------------
Command: show virtual-chassis

Virtual Chassis ID: 6c89.751e.e97c
Virtual Chassis Mode: Disables
                                                Mstr           Mixed Route Neighbor List
Member ID  Status   Serial No    Model          prio  Role      Mode  Mode ID  Interface
0 (FPC 0)  Prsnt    817789208176 vqfx-10000     128   Master*      N  VC

Member ID for next new member: 1 (FPC 1)

--------------------------------------------------

"""
    # Step 7: Compare pre-check and post-check
    changes = compare_files(extract_info(pre_check_output), extract_info(post_check_output))
    save_table_to_file(changes, "version_comparison.txt")

    print("Upgrade process completed successfully.")


if __name__ == "__main__":
    main()
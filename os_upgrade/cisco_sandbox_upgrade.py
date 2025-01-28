import sys
import time
import json  # Import JSON library
from paramiko import client, ssh_exception  # type: ignore
from getpass import getpass
import socket
import datetime
import os

os.chdir('02_file_operations/backup_files')  # Change directory to store backup files
username = input("Enter Username:")

if not username:
    username = 'admin'
    print(f"No username provided, considering default username {username}")

password = getpass(f"\U0001F511 Enter password of the user {username}: ") or "C1sco12345"

cmd_switch_01 = ['sh run']

def cisco_cmd_exicuter(hostname, commands):
    try:
        print(f"Connecting to the device {hostname}..... ")
        now = datetime.datetime.now().replace(microsecond=0)  # Current date and time without microseconds
        current_conf_file = f"{hostname}_{now}.json"  # JSON file name with timestamp
        ssh_client = client.SSHClient()
        ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())
        ssh_client.connect(hostname=hostname,
                           username=username,
                           password=password,
                           look_for_keys=False, allow_agent=False)

        print(f"Connected to the device\t{hostname} ")

        device_access = ssh_client.invoke_shell()
        device_access.send("terminal len 0\n")
        time.sleep(1)

        output_data = {}  # Dictionary to hold structured data
        for cmd in commands:
            device_access.send(f"{cmd}\n")
            time.sleep(2)  # Ensure the command output is received
            output = device_access.recv(65535).decode()  # Decode the output
            output_lines = output.splitlines()
            
            # Extract structured data
            output_data[cmd] = {
                "command": cmd,
                "output": "\n".join(output_lines[2:])  # Remove first 2 lines (prompt and echoed command)
            }
            print("\n".join(output_lines), end='')  # Print the output for reference

        # Write structured data to JSON file
        with open(current_conf_file, 'w') as json_file:
            json.dump(output_data, json_file, indent=4)
        print(f"\nConfiguration saved to {current_conf_file}")

        ssh_client.close()

    except ssh_exception.AuthenticationException:
        print("\U00002757\U00002757\U00002757Authentication failed, Check your credentials \U00002757\U00002757\U00002757")
    except socket.gaierror:
        print("\U00002757\U00002757\U00002757Check the hostname \U00002757\U00002757\U00002757")
    except ssh_exception.NoValidConnectionsError:
        print("\U00002757\U00002757\U00002757SSH Port not reachable\U00002757\U00002757\U00002757")
    except:
        print("\U00002757\U00002757\U00002757Exception Occured \U00002757\U00002757\U00002757")
        print(sys.exc_info())

cisco_cmd_exicuter('devnetsandboxiosxe.cisco.com', cmd_switch_01)

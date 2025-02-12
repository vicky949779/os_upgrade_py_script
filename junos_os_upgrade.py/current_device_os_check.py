# from jnpr.junos import Device # type: ignore
# from jnpr.junos.utils.fs import FS # type: ignore
# from getpass import getpass

# # User input
# host = input("Enter device IP: ")
# username = input("Enter username: ")
# password = getpass("Enter password: ")
# target_version = input("Enter the OS version you want to check: ")

# # Connect to the device
# dev = Device(host=host, user=username, passwd=password)
# print("Connecting.......")
# dev.open()
# print('.//////////////.......connecting  successfully..........//////////////......')
# # Get file system details
# fs = FS(dev)
# file_list = fs.ls("/var/tmp")  # Typically, OS images are stored in /var/tmp

# # Extract available OS versions
# available_versions = []
# os_files = {}

# for file in file_list:
#     if "jinstall" in file:  # Junos OS filenames usually contain "jinstall"
#         available_versions.append(file)
#         os_files[file] = f"/var/tmp/{file}"  # Store path

# dev.close()

# # Check if the requested version exists
# match_found = None
# for os_file in available_versions:
#     if target_version in os_file:
#         match_found = os_file
#         break

# # Print results
# if match_found:
#     print("\n✅ OS Version Found!")
#     print(f"📄 Version: {match_found}")
#     print(f"📂 File Path: {os_files[match_found]}")
# else:
#     print("\n❌ Not available: This OS is not found in the device.")
#     print("\n📢 Available OS versions:")
#     for index, version in enumerate(available_versions, start=1):
#         print(f"  {index}. {version}")

# from jnpr.junos import Device
# from jnpr.junos.utils.fs import FS
# from jnpr.junos.utils.sw import SW
# import sys

# # Connect to the Junos device
# dev = Device(host="192.168.40.152", user="admin", password="Abcd@123")

# try:
#     dev.open()
#     print(".....///////////////////......Connected.......////////////////..........")
#     fs = FS(dev)


#     # Get the filename at runtime
#     file_name = input("Enter the filename to check: ")
#     file_path = f"/var/tmp/{file_name}"  # Assuming files are in /var/tmp

#     # Get the list of files in /var/tmp
#     files = fs.ls('/var/tmp')

#     if file_name in files:
#         print(f"✔️ Match found: {file_name} exists on the device.")
#         print(f"🔄 Installing software: {file_path} and rebooting...")

#         # sw = SW(dev)
#         # success = sw.install(package=file_path, validate=True, reboot=True)

#         if success:
#             print("✅ Software installed successfully, rebooting initiated!")
#         else:
#             print("❌ Software installation failed.")

#     else:
#         print(f"❌ No match: {file_name} not found on the device.")

# except Exception as e:
#     print(f"Error: {e}")

# finally:
#     dev.close()
# #################################################
# from jnpr.junos import Device
# from jnpr.junos.utils.fs import FS
# from jnpr.junos.utils.sw import SW

# # Connect to the Junos device
# dev = Device(host="192.168.40.152", user="admin", password="Abcd@123")

# try:
#     dev.open()
#     print(".....///////////////////......Connected.......////////////////..........")
#     fs = FS(dev)

#     # Get the filename at runtime
#     file_name = input("Enter the filename to check: ")
#     file_path = f"/var/tmp/{file_name}"  # Assuming files are in /var/tmp

#     # Get the list of files in /var/tmp
#     files = fs.ls('/var/tmp')

#     print("\n📂 Checking files in /var/tmp/...")
    
#     match_found = False  # Flag to track if a match is found

#     for file in files:
#         print(f"🔍 Checking: {file} ...")
#         if file == file_name:
#             match_found = True
#             print(f"\n✔️ Match found: {file_name} exists on the device.")
#             print(f"🔄 Installing software: {file_path} and rebooting...")

#             # sw = SW(dev)
#             # success = sw.install(package=file_path, validate=True, reboot=True)

#             if success:
#                 print("✅ Software installed successfully, rebooting initiated!")
#             else:
#                 print("❌ Software installation failed.")

#             break  # Exit loop once a match is found

#     if not match_found:
#         print(f"\n❌ No match: {file_name} not found on the device.")

# except Exception as e:
#     print(f"Error: {e}")

# finally:
#     dev.close()
#######################################################################
# from jnpr.junos import Device
# from jnpr.junos.utils.start_shell import StartShell

# # Connect to the Junos device
# dev = Device(host="192.168.40.152", user="admin", password="Abcd@123")

# try:
#     dev.open()
#     print(".....///////////////////......Connected.......////////////////..........")

#     # Start shell session
#     with StartShell(dev) as shell:
#         # Run ls command in /var/tmp
#         output = shell.run("ls /var/tmp")[1]

#     print("\n📂 Files in /var/tmp:\n")
#     print(output)  # Print the file list

# except Exception as e:
#     print(f"Error: {e}")

# finally:
#     dev.close()

from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos.utils.sw import SW
import sys

# Connect to the Junos device
dev = Device(host="192.168.40.130", user="admin", password="Abcd@123")

try:
    dev.open()
    print(".....///////////////////......Connected.......////////////////..........")

    # Get the filename at runtime
    file_name = input("Enter the filename to check: ").strip()  # Remove extra spaces
    file_path = f"/var/tmp/{file_name}"  # Assuming files are in /var/tmp

    # Start shell session to run "ls -1 /var/tmp"
    with StartShell(dev) as shell:
        output = shell.run("ls -1 /var/tmp")[1]  # Get only command output

    # Convert output into a clean list of filenames
    files = [line.strip() for line in output.splitlines() if line.strip()]

    if file_name in files:
        print(f"✔️ Match Found: {file_name} exists in /var/tmp ✅")
        print(f"🔄 Installing software: {file_path} and rebooting...")

        # sw = SW(dev)
        # success = sw.install(package=file_path, validate=True, reboot=True)

        # if success:
        #     print("✅ Software installed successfully, rebooting initiated!")
        # else:
        #     print("❌ Software installation failed.")
    else:
        print(f"❌ No Match: {file_name} not found in /var/tmp ❌")

except Exception as e:
    print(f"Error: {e}")

finally:
    dev.close()

# import difflib
# from tabulate import tabulate  # type: ignore

# # Read the pre and post-check configuration files
# with open('precheck_outputs.txt') as g_data, open('postcheck_outputs.txt') as n_data:
#     g_config, n_config = g_data.read(), n_data.read()

# # Get differences using difflib
# delta = list(difflib.Differ().compare(g_config.splitlines(), n_config.splitlines()))

# # Prepare old and new changes with alignment
# old_changes, new_changes = [], []
# for line in delta:
#     if line.startswith("- "):
#         old_changes.append(line[1:])
#         new_changes.append("")
#     elif line.startswith("+ "):
#         new_changes.append(line[1:])
#         old_changes.append("")

# # Align lengths of old_changes and new_changes
# old_changes += [""] * (max(len(old_changes), len(new_changes)) - len(old_changes))
# new_changes += [""] * (max(len(old_changes), len(new_changes)) - len(new_changes))

# # Filter and align non-empty changes
# final_old_changes, final_new_changes = zip(*[(old, new) for old, new in zip(old_changes, new_changes) if old.strip() or new.strip()])

# # Print the table
# print(tabulate(list(zip(final_new_changes[1:], final_old_changes)), headers=["New Changes (+)", "Old Changes (-)"], tablefmt="grid"))




import difflib
from tabulate import tabulate  # type: ignore

def compare_configs(precheck_file, postcheck_file):
    # Read the pre and post-check configuration files
    with open(precheck_file) as g_data, open(postcheck_file) as n_data:
        g_config, n_config = g_data.read(), n_data.read()

    # Get differences using difflib
    delta = list(difflib.Differ().compare(g_config.splitlines(), n_config.splitlines()))

    # Prepare old and new changes with alignment
    old_changes, new_changes = [], []
    for line in delta:
        if line.startswith("- "):
            old_changes.append(line[1:])
            new_changes.append("")
        elif line.startswith("+ "):
            new_changes.append(line[1:])
            old_changes.append("")

    # Align lengths of old_changes and new_changes
    old_changes += [""] * (max(len(old_changes), len(new_changes)) - len(old_changes))
    new_changes += [""] * (max(len(old_changes), len(new_changes)) - len(new_changes))

    # Filter and align non-empty changes
    final_old_changes, final_new_changes = zip(*[(old, new) for old, new in zip(old_changes, new_changes) if old.strip() or new.strip()])

    # Print the table
    print(tabulate(list(zip(final_new_changes[1:], final_old_changes)), headers=["New Changes (+)", "Old Changes (-)"], tablefmt="grid"))

# Call the function with file paths
compare_configs('precheck_outputs.txt', 'postcheck_outputs.txt')

# import difflib
# from tabulate import tabulate  # type: ignore

# def compare_files(pre_data, post_data):
#     """Compare pre-check and post-check data."""
#     changes = []
#     max_lines = max(len(pre_data), len(post_data))
 
#     for i in range(max_lines):
#         pre_line = pre_data[i] if i < len(pre_data) else ""
#         post_line = post_data[i] if i < len(post_data) else ""
       
#         if pre_line != post_line:
#             changes.append((pre_line, post_line))
   
#     return changes

# def save_table_to_file(changes, output_file):
#     """Save changes in a table format to a file with text wrapping."""
#     col_width = 50
#     table_width = 2 * col_width + 7  # Includes borders and separator
 
#     with open(output_file, "w") as f:
#         # Write top border
#         f.write("+" + "-" * (table_width - 2) + "+\n")
 
#         # Write header row
#         header = f"| {'Pre-Check':<{col_width}} | {'Post-Check':<{col_width}} |\n"
#         f.write(header)
#         f.write("+" + "-" * (table_width - 2) + "+\n")
 
#         # Write data rows with text wrapping
#         for pre, post in changes:
#             pre_lines = wrap_text(pre, col_width)
#             post_lines = wrap_text(post, col_width)
#             max_lines = max(len(pre_lines), len(post_lines))
 
#             for i in range(max_lines):
#                 pre_line = pre_lines[i] if i < len(pre_lines) else ""
#                 post_line = post_lines[i] if i < len(post_lines) else ""
#                 f.write(f"| {pre_line:<{col_width}} | {post_line:<{col_width}} |\n")
 
#         # Write bottom border
#         f.write("+" + "-" * (table_width - 2) + "+\n")
 
#     print(f"Comparison saved to {output_file}")

# def wrap_text(text, width):
#     """Wrap text to fit within the specified width."""
#     import textwrap
#     return textwrap.wrap(text, width)

# def compare_configs(precheck_file, postcheck_file):
#     """Compare pre-check and post-check configuration files."""
#     # Read the pre and post-check configuration files
#     with open(precheck_file) as g_data, open(postcheck_file) as n_data:
#         pre_data = g_data.read().splitlines()
#         post_data = n_data.read().splitlines()

#     # Get differences using difflib
#     delta = list(difflib.Differ().compare(pre_data, post_data))

#     # Prepare old and new changes with alignment
#     old_changes, new_changes = [], []
#     for line in delta:
#         if line.startswith("- "):
#             old_changes.append(line[2:])
#             new_changes.append("")
#         elif line.startswith("+ "):
#             new_changes.append(line[2:])
#             old_changes.append("")

#     # Align lengths of old_changes and new_changes
#     old_changes += [""] * (max(len(old_changes), len(new_changes)) - len(old_changes))
#     new_changes += [""] * (max(len(old_changes), len(new_changes)) - len(new_changes))

#     # Filter and align non-empty changes
#     final_old_changes, final_new_changes = zip(*[(old, new) for old, new in zip(old_changes, new_changes) if old.strip() or new.strip()])

#     # Save the comparison results to a file
#     save_table_to_file(list(zip(final_new_changes, final_old_changes)), "version_comparison.txt")

# # Call the function with file paths
# compare_configs('precheck_outputs.txt', 'postcheck_outputs.txt')

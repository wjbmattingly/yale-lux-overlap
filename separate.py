import os
import sys
from anytree.render import RenderTree
from src.download import extract_entries
from src.visualize import create_tree
from src.clean import check_parentheses, extract_parentheticals, remove_parentheticals, move_lastname, extract_name_parts

def process_url(url, output='output.txt'):

    # Download entries from the given URL
    entries = extract_entries(url)
    # Process entries
    entries = check_parentheses(entries)
    entries = extract_parentheticals(entries)
    entries = remove_parentheticals(entries)
    entries = move_lastname(entries)
    entries = extract_name_parts(entries)

    # Create tree
    tree = create_tree(entries)

    # Check if output file exists
    if os.path.exists(output):
        print(f"Warning: Overwriting existing file {output}")


    output_branches = []
    # Print the tree
    for pre, _, node in RenderTree(tree):
        output_branches.append(f"{pre}{node.name}")

    output_str = "\n".join(output_branches)

    print(output_str)
    with open(output, 'w') as f:
        f.write(output_str)

    print(f"Tree saved to {output}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python separate.py <url> [output]")
        sys.exit(1)

    url = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else 'output.txt'
    process_url(url, output)

import os
import sys
from anytree.render import RenderTree
from src.download import extract_entries
from src.visualize import create_tree
from src.clean import check_parentheses, extract_parentheticals, remove_parentheticals, move_lastname, extract_name_parts, standardize_abbreviations, remove_dates

def process_url(url, output='output.txt'):

    # Download entries from the given URL
    entries = extract_entries(url)

    # Process entries
    entries = standardize_abbreviations(entries)
    entries = remove_dates(entries)
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

    overlap_output = f'{output.replace(".txt", "")}_overlap.txt'
    overlap_branches = []

    # Iterate through the tree to find instances where the final child has 2 or more nodes
    for pre, _, node in RenderTree(tree):
        if node.is_leaf and node.parent and len(node.parent.children) > 1:
            if node == node.parent.children[-1]:  # Check if it's the last child
                parent = node.parent
                overlap_branches.append(f"── {parent.name}")
                for child in parent.children:
                    overlap_branches.append(f"   └── {child.name}")

    overlap_str = "\n".join(overlap_branches)

    print(overlap_str)
    with open(overlap_output, 'w') as f:
        f.write(overlap_str)

    print(f"Simplified overlap structure saved to {overlap_output}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python separate.py <url> [output]")
        sys.exit(1)

    url = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else 'output.txt'
    process_url(url, output)

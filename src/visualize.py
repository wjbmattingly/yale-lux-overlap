from anytree import Node
import itertools

def create_tree(entries, consider_dates=True):
    
    entries = [entry for entry in entries if entry['type'] == 'person' and entry["manual_review"] == False]
    root = Node("Names")
    
    # Group entries by last name
    last_name_groups = itertools.groupby(sorted(entries, key=lambda x: x['last_name'] or ''), key=lambda x: x['last_name'] or '')
    
    for last_name, group in last_name_groups:
        last_name_node = Node(last_name, parent=root)
        
        # Convert group iterator to list for multiple uses
        group_list = list(group)
        
        # Group by expanded name if it exists, otherwise by other names
        name_groups = itertools.groupby(
            sorted(group_list, key=lambda x: (x['last_name'] or '', x['first_name'] or '', x['middle_name'] or '', x.get('parentheticals', [''])[0] if x.get('parentheticals') else '')),
            key=lambda x: (x['last_name'] or '', x['first_name'] or '', x['middle_name'] or '', x.get('parentheticals', [''])[0] if x.get('parentheticals') else '')
        )
        
        for name, subgroup in name_groups:
            if name:  # Only create a node if there's a name to use
                if name[3]: 
                    name_node = Node(f"{name[1]} {name[2]} {name[0]} ({name[3]})".strip(), parent=last_name_node)
                else:
                    name_node = Node(f"{name[1]} {name[2]} {name[0]}".strip(), parent=last_name_node)
                
                # Convert subgroup iterator to list for multiple uses
                subgroup_list = list(subgroup)
                
                if consider_dates:
                    # Further group by dates
                    date_groups = itertools.groupby(
                        sorted(subgroup_list, key=lambda x: x.get('dates', '') or ''),
                        key=lambda x: x.get('dates', '') or ''
                    )
                    
                    for date, date_subgroup in date_groups:
                        if date:  # Only create a node if there's a date to use
                            Node(f"{date}", parent=name_node)
                        else:
                            # If no date, add entries directly under the name node
                            for entry in date_subgroup:
                                Node(entry['name'], parent=name_node)
                else:
                    # If not considering dates, add all entries under the name node
                    for entry in subgroup_list:
                        Node(entry['name'], parent=name_node)
            else:
                # If no expanded or other names, add entries directly under the last name node
                for entry in subgroup:
                    Node(entry['name'], parent=last_name_node)
    
    return root
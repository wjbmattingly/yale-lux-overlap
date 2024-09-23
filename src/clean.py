import re
from nameparser import HumanName

def remove_dates(entries):
    """
    Removes date patterns from the 'name' field in each entry and adds a new field 'dates_removed'.

    Args:
        entries (list): A list of dictionaries containing the extracted data.

    Returns:
        list: The updated list of dictionaries with the 'dates_removed' field added.
    """
    date_pattern = re.compile(r', \b\d{4}(?:-\d{4})?\b')

    for entry in entries:
        if 'name' in entry and entry['name'] and entry['type'] == 'person':
            entry['dates_removed'] = date_pattern.sub('', entry['name']).strip()
            entry['dates_removed'] = entry['dates_removed'].rstrip('-').strip()


    return entries

def standardize_abbreviations(entries):
    """
    Standardizes all instances of abbreviations in the 'name' field of each entry to ensure there is just one white space between initials.

    Args:
        entries (list): A list of dictionaries containing the extracted data.

    Returns:
        list: The updated list of dictionaries with standardized abbreviations in the 'name' field.
    """
    abbreviation_pattern = re.compile(r'\b([A-Z])(\.)(?=[A-Z])')

    for entry in entries:
        if 'name' in entry and entry['name']:
            entry['name'] = abbreviation_pattern.sub(r'\1. ', entry['name'])

    return entries


def check_parentheses(entries):
    """
    Checks if the number of open and close parentheses in the 'name' field of each entry are the same.
    Adds a 'manual_review' flag to each entry.

    Args:
        entries (list): A list of dictionaries containing the extracted data.

    Returns:
        list: The updated list of dictionaries with the 'manual_review' field added.
    """
    for entry in entries:
        if 'name' in entry and entry['name'] and entry['type'] == 'person':
            open_parentheses = entry['name'].count('(')
            close_parentheses = entry['name'].count(')')
            entry['manual_review'] = open_parentheses != close_parentheses

    return entries

def extract_parentheticals(entries):
    """
    Extracts all parenthetical items from the 'name' field of each entry and stores them in a 'parentheticals' field.

    Args:
        entries (list): A list of dictionaries containing the extracted data.

    Returns:
        list: The updated list of dictionaries with the 'parentheticals' field added.
    """
    parenthetical_pattern = re.compile(r'\((.*?)\)')

    for entry in entries:
        if 'name' in entry and entry['name']:
            parentheticals = parenthetical_pattern.findall(entry['name'])
            entry['parentheticals'] = parentheticals

    return entries



def remove_parentheticals(entries):
    """
    Removes parenthetical and bracketed items from the 'dates_removed' field of each entry and stores the result in a 'clean_name' field.
    Also removes any trailing white space and instances of " ,".

    Args:
        entries (list): A list of dictionaries containing the extracted data.

    Returns:
        list: The updated list of dictionaries with the 'clean_name' field added.
    """
    
    parenthetical_pattern = re.compile(r'\(.*?\)')
    bracket_pattern = re.compile(r'[\[\]]')

    for entry in entries:
        if 'name' in entry and entry['name'] and entry['type'] == 'person':
            if 'dates_removed' in entry and entry['dates_removed']:
                entry['dates_removed'] = entry['dates_removed'].replace(', (', ' (').strip()
                clean_name = parenthetical_pattern.sub('', entry['dates_removed']).strip()
                clean_name = bracket_pattern.sub('', clean_name).strip()
                clean_name = clean_name.replace(' ,', '').strip()

                entry['clean_name'] = clean_name
            else:
                entry['name'] = entry['name'].replace(', (', ' (').strip()
                clean_name = parenthetical_pattern.sub('', entry['name']).strip()
                clean_name = bracket_pattern.sub('', clean_name).strip()
                clean_name = clean_name.replace(' ,', '').strip()
                entry['clean_name'] = clean_name

    return entries

def move_lastname(entries):
    """
    Checks if a last name appears first in the 'clean_name' field of each entry and moves it to the end if it does.

    Args:
        entries (list): A list of dictionaries containing the extracted data.

    Returns:
        list: The updated list of dictionaries with the 'clean_name' field modified.
    """
    for entry in entries:
        if 'clean_name' in entry and entry['clean_name'] and entry['type'] == 'person':
            clean_name = entry['clean_name']
            if ',' in clean_name:
                parts = clean_name.split(',', 1)
                if len(parts) == 2:
                    last_name = parts[0].strip()
                    rest_of_name = parts[1].strip()
                    entry['clean_name'] = f"{rest_of_name} {last_name}"
    return entries




def extract_name_parts(entries):
    for entry in entries:
        if 'clean_name' in entry and entry['clean_name'] and entry['type'] == 'person':
            name_parts = HumanName(entry['clean_name'])
            name_parts = name_parts.as_dict()
            entry['last_name'] = name_parts.get('last', None)
            entry['first_name'] = name_parts.get('first', None)
            entry['middle_name'] = name_parts.get('middle', None)
            entry['suffix'] = name_parts.get('suffix', None)
            entry['nickname'] = name_parts.get('nickname', None)
    return entries
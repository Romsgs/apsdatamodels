# get_element_groups.py

from autodesk_api import (
    get_access_token,
    get_root_element_group,
    get_element_group_children,
)
import sys

def traverse_element_groups(access_token, project_id, group_id, level=0):
    """
    Recursively traverse and display the element groups hierarchy.
    """
    # Get children of the current group
    children_data = get_element_group_children(access_token, project_id, group_id)
    if not children_data:
        return

    children = children_data.get('data', [])
    for child in children:
        group_name = child['attributes'].get('name', 'Unnamed Group')
        child_group_id = child['id']
        indent = '  ' * level
        print(f"{indent}- {group_name} (ID: {child_group_id})")
        # Recursively traverse child groups
        traverse_element_groups(access_token, project_id, child_group_id, level + 1)

def main():
    # Step 1: Authenticate and get access token
    access_token = get_access_token()
    if not access_token:
        print('Exiting due to authentication failure.')
        return

    if len(sys.argv) != 2:
        print('Usage: python get_element_groups.py <project_id>')
        return

    project_id = sys.argv[1]

    # Step 2: Get the root element group
    root_group_data = get_root_element_group(access_token, project_id)
    if not root_group_data:
        print('Exiting due to failure in retrieving the root element group.')
        return

    root_group = root_group_data.get('data', {})
    root_group_id = root_group.get('id')
    root_group_name = root_group['attributes'].get('name', 'Root Group')

    print(f"Root Element Group: {root_group_name} (ID: {root_group_id})")

    # Step 3: Traverse and display the element group hierarchy
    traverse_element_groups(access_token, project_id, root_group_id)

if __name__ == '__main__':
    main()

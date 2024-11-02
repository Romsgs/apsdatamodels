"""
main.py

A script to authenticate with Autodesk API, retrieve hubs and projects, and navigate through
element groups within a selected project.

Functions:
    - traverse_element_groups: Recursively traverses and displays the element groups hierarchy.
    - main: Orchestrates the authentication, hub retrieval, project selection,
      and element group navigation.

Usage:
    Run the script and follow the on-screen prompts to explore element groups within a project.
"""


import logging
from autodesk_api import (
    get_access_token,
    get_hubs,
    get_projects,
    get_root_element_group,
    get_element_group_children,
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def traverse_element_groups(access_token, project_id, group_id, level=0):
    """
    Recursively traverse and display the element groups hierarchy within a project.

    This function retrieves the child element groups of the specified `group_id` within the
    given `project_id` and prints their names and IDs. It uses indentation to represent the
    depth of each group in the hierarchy.

    Args:
        access_token (str): The OAuth 2.0 access token for authenticating API requests.
        project_id (str): The unique identifier of the project whose element groups are 
        being traversed.
        group_id (str): The unique identifier of the current element group to retrieve 
        children from.
        level (int, optional): The current depth level in the hierarchy for indentation purposes.
            Defaults to 0.

    Returns:
        None

    Raises:
        None

    Example:
        traverse_element_groups(access_token, "b.1234", "eg.5678", level=1)
    """
    # Get children of the current group
    children_data = get_element_group_children(access_token, project_id, group_id)
    if not children_data:
        logging.warning(f"No children found for element group ID: {group_id}")
        return

    children = children_data.get('data', [])
    for child in children:
        group_name = child['attributes'].get('name', 'Unnamed Group')
        child_group_id = child['id']
        indent = '  ' * level
        logging.info(f"{indent}- {group_name} (ID: {child_group_id})")
        # Recursively traverse child groups
        traverse_element_groups(access_token, project_id, child_group_id, level + 1)


def main():
    """
    Main function to authenticate, retrieve hubs and projects, and navigate element groups within a project.

    The function performs the following steps:
        1. Authenticates with the Autodesk API to obtain an access token.
        2. Retrieves the list of hubs associated with the authenticated account.
        3. Selects the first hub (assuming only one exists).
        4. Retrieves the list of projects within the selected hub.
        5. Prompts the user to select a project from the list.
        6. Retrieves the root element group of the selected project.
        7. Recursively traverses and displays the hierarchy of element groups within the project.

    Args:
        None

    Returns:
        None

    Raises:
        None

    Usage:
        Run the script and follow the on-screen prompts to navigate through element groups.

    Example:
        python main.py
    """
    # Step 1: Authenticate and get access token
    access_token = get_access_token()
    if not access_token:
        logging.error('Exiting due to authentication failure.')
        return

    # Step 2: Retrieve hubs
    hubs_data = get_hubs(access_token)
    if not hubs_data:
        logging.error('Exiting due to failure in retrieving hubs.')
        return

    hubs = hubs_data.get('data', [])
    if not hubs:
        logging.error('No hubs found.')
        return

    # Since there's only one hub, select it directly
    selected_hub = hubs[0]
    hub_id = selected_hub['id']
    hub_name = selected_hub['attributes'].get('name', 'Unnamed Hub')
    logging.info(f'Selected Hub: {hub_name} (ID: {hub_id})')

    # Step 3: Retrieve projects from the selected hub
    projects_data = get_projects(access_token, hub_id)
    if not projects_data:
        logging.error('Exiting due to failure in retrieving projects.')
        return

    projects = projects_data.get('data', [])
    if not projects:
        logging.error('No projects found in the selected hub.')
        return

    # Display the list of projects and allow the user to select one
    logging.info('\nAvailable Projects:')
    for idx, project in enumerate(projects):
        project_name = project['attributes']['name']
        project_id = project['id']
        logging.info(f'{idx + 1}. {project_name} (ID: {project_id})')

    # Prompt the user to select a project
    try:
        project_choice = int(input('\nEnter the number of the project you want to explore: ')) - 1
        if not 0 <= project_choice < len(projects):
            raise ValueError
    except ValueError:
        logging.error('Invalid selection.')
        return

    selected_project = projects[project_choice]
    project_id = selected_project['id']
    project_name = selected_project['attributes']['name']
    logging.info(f'\nSelected Project: {project_name} (ID: {project_id})')

    # Step 4: Get the root element group
    root_group_data = get_root_element_group(access_token, project_id)
    if not root_group_data:
        logging.error('Exiting due to failure in retrieving the root element group.')
        return

    root_group = root_group_data.get('data', {})
    root_group_id = root_group.get('id')
    root_group_name = root_group['attributes'].get('name', 'Root Group')

    logging.info(f'\nRoot Element Group: {root_group_name} (ID: {root_group_id})\n')

    # Step 5: Traverse and display the element group hierarchy
    traverse_element_groups(access_token, project_id, root_group_id)


if __name__ == '__main__':
    main()

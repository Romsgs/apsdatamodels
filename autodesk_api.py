# autodesk_api.py

import requests
from config import CLIENT_ID, CLIENT_SECRET

DEFAULT_TIMEOUT = 10  # Adjust as needed

def get_access_token():
    """
    Obtain an access token from the Autodesk Authentication API (OAuth v2).
    """
    url = "https://developer.api.autodesk.com/authentication/v2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "data:read data:write data:create data:search",
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        access_token = response.json()["access_token"]
        print("Access token retrieved successfully.")
        return access_token
    except requests.exceptions.Timeout:
        print("Request timed out while trying to retrieve access token.")
        return None
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve access token.")
        print("Error:", e)
        return None

def get_hubs(access_token):
    """
    Retrieve a list of hubs using the access token.
    """
    url = "https://developer.api.autodesk.com/project/v1/hubs"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        hubs = response.json()
        print("Hubs retrieved successfully.")
        return hubs
    except requests.exceptions.Timeout:
        print("Request timed out while trying to retrieve hubs.")
        return None
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve hubs.")
        print("Error:", e)
        return None

def get_projects(access_token, hub_id):
    """
    Retrieve projects from a specific hub.
    """
    url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        projects = response.json()
        print("Projects retrieved successfully.")
        return projects
    except requests.exceptions.Timeout:
        print("Request timed out while trying to retrieve projects.")
        return None
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve projects.")
        print("Error:", e)
        return None

def get_root_element_group(access_token, project_id):
    """
    Retrieve the root element group of a project.
    """
    url = f"https://developer.api.autodesk.com/element/v1/projects/{project_id}/elementGroups/root"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        root_group = response.json()
        print("Root element group retrieved successfully.")
        return root_group
    except requests.exceptions.Timeout:
        print("Request timed out while trying to retrieve the root element group.")
        return None
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve the root element group.")
        print("Error:", e)
        return None

def get_element_group_children(access_token, project_id, group_id):
    """
    Retrieve the child element groups of a specific element group.
    """
    url = f"https://developer.api.autodesk.com/element/v1/projects/{project_id}/elementGroups/{group_id}/children"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        children = response.json()
        print(f"Children of element group {group_id} retrieved successfully.")
        return children
    except requests.exceptions.Timeout:
        print(f"Request timed out while trying to retrieve children of element group {group_id}.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve children of element group {group_id}.")
        print("Error:", e)
        return None

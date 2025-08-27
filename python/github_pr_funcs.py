import re
import requests
import json
from pprint import pprint

def separate_raw_pr_url(raw_pr_url):
    """
    Take a raw pr url of the form:  
        https://github.com/ucsb-cs156-s25/proj-dining-s25-10/pull/46
    separates it into its components, and returns the components as a dictionary
    Args:
        raw_pr_url (str): The raw URL of the pull request.
    Returns:
        dict: A dictionary containing the components of the pull request URL.
    """

    # use a regular expression to extract the components

    pattern = r"https://github\.com/(?P<org>[^/]+)/(?P<repo>[^/]+)/pull/(?P<pr_number>\d+)"
    match = re.match(pattern, raw_pr_url)
    if not match:
        raise ValueError(f"Invalid GitHub pull request URL format: <{raw_pr_url}>")
    components = match.groupdict()
    components['org'] = components['org'].lower()  # convert org to lowercase
    components['repo'] = components['repo'].lower()  # convert repo to lowercase
    components['pr_number'] = components['pr_number'].strip()  # strip whitespace
    return components    
    


def get_pr_from_raw_pr_url(GITHUB_TOKEN, raw_pr_url):
    """
    Take a raw pr url of the form:
    
    https://github.com/ucsb-cs156-s25/proj-dining-s25-10/pull/46
    
    separates it into its components, and then uses the Github API to get 
    information about the pull request as a dictionary.
    
    Args:
        raw_pr_url (str): The raw URL of the pull request.
        
    Returns:
        int: The pull request number.
    """
    
    components = separate_raw_pr_url(raw_pr_url)
    
    url = f"https://api.github.com/repos/{components['org']}/{components['repo']}/pulls/{components['pr_number']}"    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch pull request: {response.status_code} {response.text}")
    pr_data = response.json()
    return pr_data


def get_dokku_link_from_pr_data(pr_data):
    """
    Extracts the dokku link from the pull request data.
    
    Args:
        pr_data (dict): The pull request data as a dictionary.
        
    Returns:
        str: The dokku link if found, otherwise None.
    """
    
    pattern = r"https://(?P<appname>[^\.]+)\.dokku-(?P<dokku_num>\d\d).cs.ucsb.edu"    
    body = pr_data.get('body', '')
    match = re.search(pattern, body)    
    if not match:
        return None
    return match.groupdict()


def get_parts_from_repo_name(repo_name):
    """
    Extracts the organization and repository name from a repository name.
    
    Args:
        repo_name (str): The repository name in the format 'org/repo'.
        
    Returns:
        tuple: A tuple containing the organization and repository name.
    """
    pattern = r"proj-(?P<projname>[^\-]+)-(?P<qxx>[fwsm]\d\d)-(?P<team_num>\d\d)"    
    match = re.search(pattern, repo_name)    
    if not match:
        return None
    return match.groupdict()
 

def get_dokku_command_elements_from_raw_pr_url(GITHUB_TOKEN, raw_pr_url):
    """
    Extracts the dokku command from the raw pull request URL.
    
    Args:
        raw_pr_url (str): The raw URL of the pull request.
        
    Returns:
        str: The dokku command if found, otherwise None.
    """

    raw_pr_url_components = separate_raw_pr_url(raw_pr_url)    
    repo_name_components = get_parts_from_repo_name(raw_pr_url_components['repo'])
    pr_data = get_pr_from_raw_pr_url(GITHUB_TOKEN, raw_pr_url)
    dokku_app = get_dokku_link_from_pr_data(pr_data)
        
    if dokku_app['dokku_num']!="00" and  dokku_app['dokku_num'] != repo_name_components['team_num']:
        raise ValueError(f"Dokku number {dokku_app['dokku_num']} does not match team number {repo_name_components['team_num']} in repo name {raw_pr_url_components['repo']}")
    appname = dokku_app['appname']
    dokku_num = dokku_app['dokku_num']
    repo_url = f"https://github.com/{raw_pr_url_components['org']}/{raw_pr_url_components['repo']}"
    try:
        branch = pr_data['head']['ref'] 
    except KeyError:
        raise ValueError("Could not find branch name for PR with URL: " + raw_pr_url)
    
    return json.dumps({
        "app": appname,
        "dokku": dokku_num,
        "repo": repo_url,
        "branch": branch,
        "owner": raw_pr_url_components['org'],
        "repo_name": raw_pr_url_components['repo'],
        "pr_url": raw_pr_url,
    })
    
def get_repo_and_branch_from_raw_pr_url(GITHUB_TOKEN, raw_pr_url):
    """
    Extracts the repo and branch from the raw pull request URL.
    
    Args:
        raw_pr_url (str): The raw URL of the pull request.
        
    Returns:
        str: The dokku command if found, otherwise None.
    """

    raw_pr_url_components = separate_raw_pr_url(raw_pr_url)    
    pr_data = get_pr_from_raw_pr_url(GITHUB_TOKEN, raw_pr_url)
    repo_url = f"https://github.com/{raw_pr_url_components['org']}/{raw_pr_url_components['repo']}"
    try:
        branch = pr_data['head']['ref'] 
    except KeyError:
        raise ValueError("Could not find branch name for PR with URL: " + raw_pr_url)
    
    return json.dumps({
        "repo": repo_url,
        "branch": branch
    })
  
if __name__ == "__main__":
    with open("GITHUB_TOKEN", "r") as f:
        GITHUB_TOKEN = f.read().strip()
    raw_pr_url = "https://github.com/ucsb-cs156-s25/proj-dining-s25-04/pull/40";
    
    dokku_command = get_dokku_command_elements_from_raw_pr_url(GITHUB_TOKEN, raw_pr_url)
    print(dokku_command)

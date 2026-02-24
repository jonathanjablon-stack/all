import os
import requests

USERNAME = 'jonathanjablon-stack'
TOKEN = os.environ.get('GH_PAT')
HEADERS = {'Authorization': f'token {TOKEN}'}

def get_repos():
    # Fetches all repos for the user
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_html_files(repo_name, default_branch):
    # Fetches the file tree for a specific repo
    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/git/trees/{default_branch}?recursive=1"
    response = requests.get(url, headers=HEADERS)
    tree = response.json().get('tree', [])
    return [file['path'] for file in tree if file['path'].endswith('.html')]

def generate_html():
    repos = get_repos()
    html_content = "<html><head><title>My Master Directory</title></head><body><h1>All HTML Files</h1>"
    
    for repo in repos:
        repo_name = repo['name']
        branch = repo.get('default_branch', 'main')
        html_files = get_html_files(repo_name, branch)
        
        if html_files:
            html_content += f"<h2>{repo_name}</h2><ul>"
            for file in html_files:
                # Creates a link to the raw HTML file or GitHub pages
                link = f"https://jonathanjablon-stack.github.io/{repo_name}/{file}" 
                html_content += f"<li><a href='{link}'>{file}</a></li>"
            html_content += "</ul>"
            
    html_content += "</body></html>"
    
    with open('index.html', 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_html()

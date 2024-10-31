import requests
import pandas as pd
import os

# Load GitHub token from environment
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
print(GITHUB_TOKEN)
HEADERS = {'Authorization': f'Bearer {GITHUB_TOKEN}'}


def fetch_users():
    users_data = []
    page = 1  # Start from the first page
    while True:
        url = f"https://api.github.com/search/users?q=location:melbourne followers:>100&per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        data = response.json()

        # Stop if there are no more users to fetch
        if 'items' not in data or not data['items']:
            break

        for item in data['items']:
            # Fetch detailed user data
            user_url = f"https://api.github.com/users/{item['login']}"
            user_data = requests.get(user_url, headers=HEADERS).json()
            users_data.append({
                'login': user_data['login'],
                'name': user_data.get('name', ''),
                'company': format_company_name(user_data.get('company', '')),
                'location': user_data.get('location', ''),
                'email': user_data.get('email', ''),
                'hireable': user_data.get('hireable', ''),
                'bio': clean_text(user_data.get('bio', '')),
                'public_repos': user_data.get('public_repos', 0),
                'followers': user_data.get('followers', 0),
                'following': user_data.get('following', 0),
                'created_at': user_data.get('created_at', '')
            })

        # Move to the next page
        page += 1

    return users_data


def format_company_name(company_name):
    if company_name:
        return company_name.lstrip('@').strip().upper()
    return ''


def clean_text(text):
    """Remove newline characters from the text."""
    if text:
        return text.replace('\n', ' ').replace('\r', '').strip()
    return text

def fetch_repositories(user_login):
    repos_data = []
    page = 1
    url = f"https://api.github.com/users/{user_login}/repos?per_page=100&page={page}"
    while url:
        response = requests.get(url, headers=HEADERS)
        repos = response.json()
        for repo in repos:
            repos_data.append({
                'login': user_login,
                'full_name': repo['full_name'],
                'created_at': repo['created_at'],
                'stargazers_count': repo['stargazers_count'],
                'watchers_count': repo['watchers_count'],
                'language': repo['language'],
                'has_projects': repo['has_projects'],
                'has_wiki': repo['has_wiki'],
                'license_name': repo['license']['key'] if repo['license'] else ''
            })
        # Get the next page, if available
        url = response.links.get('next', {}).get('url')
    return repos_data


# Fetch all users and store in users.csv
users_data = fetch_users()
users_df = pd.DataFrame(users_data)

# Save the cleaned DataFrame to CSV
users_df.to_csv('users.csv', index=False)


# Fetch repositories for each user and store in repositories.csv
all_repos = []
for login in users_df['login']:
    all_repos.extend(fetch_repositories(login))

repos_df = pd.DataFrame(all_repos)
repos_df.to_csv('repositories.csv', index=False)

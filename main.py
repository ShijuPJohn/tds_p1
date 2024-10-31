import requests
import pandas as pd
import os

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
print(GITHUB_TOKEN)
HEADERS = {'Authorization': f'Bearer {GITHUB_TOKEN}'}


def fetch_users():
    users_data = []
    url = 'https://api.github.com/search/users?q=location:melbourne followers:>100'
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    print(data)
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
            'bio': user_data.get('bio', ''),
            'public_repos': user_data.get('public_repos', 0),
            'followers': user_data.get('followers', 0),
            'following': user_data.get('following', 0),
            'created_at': user_data.get('created_at', '')
        })
    url = data.get('next')
    return users_data


def format_company_name(company_name):
    if company_name:
        return company_name.lstrip('@').strip().upper()
    return ''


def fetch_repositories(user_login):
    repos_data = []
    url = f"https://api.github.com/users/{user_login}/repos?per_page=100"
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
        url = response.links.get('next', {}).get('url')
    return repos_data


# Collect repositories for each user

# Save to CSV
users_df = pd.DataFrame(fetch_users())
users_df.to_csv('users.csv', index=False)
all_repos = []
for login in users_df['login']:
    all_repos.extend(fetch_repositories(login))

repos_df = pd.DataFrame(all_repos)
repos_df.to_csv('repositories.csv', index=False)

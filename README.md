# Melbourne GitHub Users and Repositories

- Data was scraped from the GitHub API by searching for users in Melbourne with over 100 followers and collecting their profiles and repositories.
- Surprisingly, many popular Melbourne-based GitHub users have inactive or very few public repositories, even with high follower counts.
- Developers seeking a larger following might consider regular updates or projects to engage with the community more actively.

## Overview

This repository contains data on GitHub users based in Melbourne with over 100 followers. The data is structured into two CSV files:

### Files
1. `users.csv`: Information about each user.
2. `repositories.csv`: Information about each user's public repositories (up to 500 most recent).

### Fields

- **users.csv**
  - `login`: User's GitHub ID
  - `name`: Full name
  - `company`: Company name (formatted)
  - `location`: City (Melbourne)
  - `email`: User's email address
  - `hireable`: Hireability status
  - `bio`: User's bio
  - `public_repos`: Number of public repositories
  - `followers`: Number of followers
  - `following`: Number of users the person is following
  - `created_at`: Date of account creation

- **repositories.csv**
  - `login`: User ID of repository owner
  - `full_name`: Full name of the repository
  - `created_at`: Repository creation date
  - `stargazers_count`: Star count
  - `watchers_count`: Watchers count
  - `language`: Repository language
  - `has_projects`: Whether projects are enabled
  - `has_wiki`: Whether wiki is enabled
  - `license_name`: License name

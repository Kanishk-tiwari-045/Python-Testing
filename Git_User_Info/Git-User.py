import requests
import json
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class GithubUser:
    # Constructor to initialize the username
    def __init__(self, username):
        self.username = username
        self.user_details = None
        self.details = None
        self.repos = None
        self.repo_events = {}
        self.commit_activity = None

    # Program to fetch details of the User
    def fetch_details(self):
        url = f"https://api.github.com/users/{self.username}"
        response = requests.get(url)
        if response.status_code == 200:
            self.user_details = response.json()
        else:
            self.user_details = None

    # Program to extract needed details of the User
    def extract_details(self):
        if not self.user_details:
            return None
        self.details = {
            'login': self.user_details.get('login'), 
            'id': self.user_details.get('id'), 
            'name': self.user_details.get('name'), 
            'company': self.user_details.get('company'), 
            'blog': self.user_details.get('blog'), 
            'location': self.user_details.get('location'), 
            'email': self.user_details.get('email'), 
            'bio': self.user_details.get('bio'), 
            'public_repos': self.user_details.get('public_repos'), 
            'followers': self.user_details.get('followers'), 
            'following': self.user_details.get('following')
        }
        return self.details

    # Program to update or add to the database
    def Database_updation(self):
        if not self.details:
            return None
        obj2 = sqlite3.connect('Users_Info.db')
        obj2.execute('''CREATE TABLE IF NOT EXISTS users(
                    login TEXT PRIMARY KEY,
                    id INTEGER,
                    name TEXT,
                    company TEXT,
                    blog TEXT,
                    location TEXT,
                    email TEXT,
                    bio TEXT,
                    public_repos INTEGER,
                    followers INTEGER,
                    following INTEGER)''')

        obj2.execute('''INSERT OR REPLACE INTO users(
                     login, id, name, company, blog, location, email, bio, public_repos, followers, following)
                     VALUES (:login, :id, :name, :company, :blog, :location, :email, :bio, :public_repos, :followers, :following)''', self.details)

        obj2.commit()

    # Program to print basic details of the User
    def print_details(self):
        if not self.details:
            return None
        final_data = json.dumps(self.details, indent=2)
        print(final_data)

    # Program to fetch repositories of a particular User
    def fetch_repo_data(self):
        url = f"https://api.github.com/users/{self.username}/repos"
        response = requests.get(url)
        if response.status_code == 200:
            self.repos = response.json()
        else:
            self.repos = None

    # Program to print repositories of a particular User with basic details
    def print_repo(self):
        if not self.repos:
            print("No repository found.")
            return
        for repo in self.repos:
            repo_details = {
                'name': repo.get('name'),
                'full_name': repo.get('full_name'),
                'description': repo.get('description'),
                'html_url': repo.get('html_url'),
                'language': repo.get('language'),
                'forks_count': repo.get('forks_count'),
                'watchers_count': repo.get('watchers_count')
            }
            print(json.dumps(repo_details, indent=2))
            
    # Program to print most used language
    def top_lang(self):
        if not self.repos:
            return None
        lang = {}
        for repo in self.repos:
            language = repo.get('language')
            if language:
                lang[language] = lang.get(language, 0) + 1
        if lang:
            most_used = max(lang, key=lang.get)
            print(f"The most used language is: {most_used}")
        else:
            print("No languages found.")

    # Program to fetch events of a particular Repository
    def fetch_repo_events(self, repo_name):
        url = f"https://api.github.com/repos/{self.username}/{repo_name}/events"
        response = requests.get(url)
        if response.status_code == 200:
            self.repo_events[repo_name] = response.json()
        else:
            self.repo_events[repo_name] = None
    
    # Program to print events of a particular Repository
    def print_repo_events(self, repo_name):
        events = self.repo_events.get(repo_name)
        if not events:
            print(f"No events in {repo_name}.")
            return
        print(f"Events in {repo_name}:")
        for event in events:
            event_details = {
                'type': event.get('type'),
                'created_at': event.get('created_at'),
                'repo': event['repo'].get('name') if 'repo' in event else 'N/A'
            }
            print(json.dumps(event_details, indent=2))

    # Program to fetch commit activity of a particular Repository
    def fetch_repo_commit_activity(self, repo_name):
        url = f"https://api.github.com/repos/{self.username}/{repo_name}/commits"
        response = requests.get(url)
        if response.status_code == 200:
            self.commit_activity = response.json()
        else:
            self.commit_activity = None

    # Program to show commits of a particular Repository
    def create_contribution_heatmap(self, commit_activity):
        if not commit_activity:
            return
        # Convert commit activity to dates
        commit_dates = [
            datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ').date()
            for commit in commit_activity
        ]
        # Count commits per day
        commit_count = pd.Series(commit_dates).value_counts().sort_index()
        # Create a DataFrame to fit into a calendar heatmap format
        commit_df = commit_count.reset_index()
        commit_df.columns = ['date', 'commits']

        # Complete with all dates of the past year
        all_dates = pd.date_range(commit_df['date'].min(), commit_df['date'].max(), freq='D')
        commit_df = commit_df.set_index('date').reindex(all_dates, fill_value=0).reset_index()
        commit_df.columns = ['date', 'commits']
        commit_df['month'] = commit_df['date'].dt.month
        commit_df['day'] = commit_df['date'].dt.day

        # Create heatmap using seaborn
        heatmap_data = commit_df.pivot(index='day', columns='month', values='commits').fillna(0)
        plt.figure(figsize=(6, 5))
        sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt="d", cbar_kws={'label': 'Commits'})
        plt.title(f'GitHub Contributions Heatmap for {self.username}/{repo_name}')
        plt.xlabel('Month')
        plt.ylabel('Day of Month')
        plt.xticks(rotation=0)
        plt.yticks(rotation=0)
        plt.show()

#Main Program
username = input("Enter the GitHub username: ")
user_obj = GithubUser(username)
user_obj.fetch_details()

if user_obj.user_details:
    user_obj.extract_details()
    user_obj.print_details()
    user_obj.Database_updation()
    print("User data has been saved.")
    user_obj.fetch_repo_data()
    show_repo = input("Do you want to see the repo data? (y/n): ").strip().lower()

    if show_repo == 'y':
        user_obj.print_repo()
        repo_name = input("Enter the repository name: ").strip()
        user_obj.fetch_repo_commit_activity(repo_name)
        user_obj.create_contribution_heatmap(user_obj.commit_activity)

        repo_events = input("Do you want to see repo events? (y/n): ").strip().lower()
        if repo_events == 'y':
            user_obj.fetch_repo_events(repo_name)
            user_obj.print_repo_events(repo_name)
else:
    print("User not found.")

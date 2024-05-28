# import requests
# import json
# import sqlite3
# import matplotlib.pyplot as plt

# class GithubUser:
# # Initialising constructor for prerequisites
#     def __init__(self, username):
#         self.username = username
#         self.user_details = None
#         self.details = None

# # Fetching all the data from the API
#     def fetch_details(self):
#         url = f"https://api.github.com/users/{self.username}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             self.user_details = response.json()
#         else:
#             self.user_details = None

# # Extracting relevant Information
#     def extract_details(self):
#         if not self.user_details:
#             return None
#         self.details = {'login': self.user_details.get('login'), 'id': self.user_details.get('id'), 'name': self.user_details.get('name'), 'company': self.user_details.get('company'), 'blog': self.user_details.get('blog'), 'location': self.user_details.get('location'), 'email': self.user_details.get('email'), 'bio': self.user_details.get('bio'), 'public_repos': self.user_details.get('public_repos'), 'followers': self.user_details.get('followers'), 'following': self.user_details.get('following')
#         }
#         return self.details

# # Saving or Updating in database
#     def Database_updation(self):
#         if not self.details:
#             return None
#         obj2 = sqlite3.connect('Users_Info.db')
#         obj2.execute('''CREATE TABLE IF NOT EXISTS users(
#                     login TEXT PRIMARY KEY,
#                     id INTEGER,
#                     name TEXT,
#                     company TEXT,
#                     blog TEXT,
#                     location TEXT,
#                     email TEXT,
#                     bio TEXT,
#                     public_repos INTEGER,
#                     followers INTEGER,
#                     following INTEGER)''')

#         obj2.execute('''INSERT OR REPLACE INTO users(
#                      login, id, name, company, blog, location, email, bio, public_repos, followers, following)
#                      VALUES (:login, :id, :name, :company, :blog, :location, :email, :bio, :public_repos, :followers, :following)''', self.details)

#         obj2.commit()

# #Printing data on the console
#     def print_details(self):
#         if not self.details:
#             return None
#         final_data = json.dumps(self.details, indent=2)
#         print(final_data)

# # Main Execution
# username = str(input("Enter the GitHub username: "))
# user_obj = GithubUser(username)
# user_obj.fetch_details()
# if(user_obj.user_details):
#     user_obj.extract_details()
#     user_obj.print_details()
#     user_obj.Database_updation()
#     print("User data has been saved.")
# else:
#     print("User not found.")


import requests
import json
import sqlite3

class GithubUser:
    def __init__(self, username):
        self.username = username
        self.user_details = None
        self.details = None
        self.repos = None
        self.repo_events = {}


    def fetch_details(self):
        url = f"https://api.github.com/users/{self.username}"
        response = requests.get(url)
        if response.status_code == 200:
            self.user_details = response.json()
        else:
            self.user_details = None


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


    def print_details(self):
        if not self.details:
            return None
        final_data = json.dumps(self.details, indent=2)
        print(final_data)


    def fetch_repo_data(self):
        url = f"https://api.github.com/users/{self.username}/repos"
        response = requests.get(url)
        if response.status_code == 200:
            self.repos = response.json()
        else:
            self.repos = None


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


    def fetch_repo_events(self, repo_name):
        url = f"https://api.github.com/repos/{self.username}/{repo_name}/events"
        response = requests.get(url)
        if response.status_code == 200:
            self.repo_events[repo_name] = response.json()
        else:
            self.repo_events[repo_name] = None


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


username = str(input("Enter the GitHub username: "))
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
    repo_events = input("Do you want to see repo events? (y/n): ").strip().lower()
    if repo_events == 'y':
        repo_name = input("Enter the repository name: ").strip()
        user_obj.fetch_repo_events(repo_name)
        user_obj.print_repo_events(repo_name)
    most_used = user_obj.top_lang()
else:
    print("User not found.")



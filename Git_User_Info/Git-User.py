import requests
import json
import sqlite3

class GithubUser:
# Initialising constructor for prerequisites
    def __init__(self, username):
        self.username = username
        self.user_details = None
        self.details = None

# Fetching all the data from the API
    def fetch_details(self):
        url = f"https://api.github.com/users/{self.username}"
        response = requests.get(url)
        if response.status_code == 200:
            self.user_details = response.json()
        else:
            self.user_details = None

# Extracting relevant Information
    def extract_details(self):
        if not self.user_details:
            return None
        self.details = {'login': self.user_details.get('login'), 'id': self.user_details.get('id'), 'name': self.user_details.get('name'), 'company': self.user_details.get('company'), 'blog': self.user_details.get('blog'), 'location': self.user_details.get('location'), 'email': self.user_details.get('email'), 'bio': self.user_details.get('bio'), 'public_repos': self.user_details.get('public_repos'), 'followers': self.user_details.get('followers'), 'following': self.user_details.get('following')
        }
        return self.details

# Saving or Updating in database
    def Database_updation(self):
        if not self.details:
            return None
        conn = sqlite3.connect('Users_Info.db')
        conn.execute('''CREATE TABLE IF NOT EXISTS users(
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

        conn.execute('''INSERT OR REPLACE INTO users(
                     login, id, name, company, blog, location, email, bio, public_repos, followers, following)
                     VALUES (:login, :id, :name, :company, :blog, :location, :email, :bio, :public_repos, :followers, :following)''', self.details)

        conn.commit()

#Printing data on the console
    def print_details(self):
        if not self.details:
            return None
        final_data = json.dumps(self.details, indent=2)
        print(final_data)

# Main Execution
username = str(input("Enter the GitHub username: "))
user_object = GithubUser(username)
user_object.fetch_details()
if(user_object.user_details):
    user_object.extract_details()
    user_object.print_details()
    user_object.Database_updation()
    print("User data has been saved.")
else:
    print("User not found.")

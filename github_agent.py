import os
import requests
from dotenv import load_dotenv
from backend.agents.base_agent import BaseAgent  # Corrected import

# Load environment variables
load_dotenv()

class GitHubAgent(BaseAgent):
    def __init__(self):
        super().__init__("GitHub Agent")
        self.token = os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise EnvironmentError("GITHUB_TOKEN is not set in environment variables.")
        
        self.api_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_recent_commits(self, owner: str, repo: str, per_page: int = 5) -> str:
        url = f"{self.api_url}/repos/{owner}/{repo}/commits"
        response = requests.get(url, headers=self.headers, params={"per_page": per_page})

        if response.status_code != 200:
            return f"GitHub API error {response.status_code}: {response.text}"

        commits = response.json()
        return "\n".join(
            f"[{commit['sha'][:7]}] {commit['commit']['message']}" for commit in commits
        )

    def get_commits_by_user(self, owner: str, repo: str, username: str, per_page: int = 5) -> str:
        """Fetch commits by a specific user in a specific repo."""
        url = f"{self.api_url}/repos/{owner}/{repo}/commits"
        params = {
            "author": username,
            "per_page": per_page
        }
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            return f"GitHub API error {response.status_code}: {response.text}"

        commits = response.json()
        if not commits:
            return f"No commits found by user '{username}' in repo '{repo}'."

        return "\n".join(
            f"[{c['sha'][:7]}] {c['commit']['message']}" for c in commits
        )

    def list_my_repos(self) -> str:
        url = f"{self.api_url}/user/repos"
        response = requests.get(url, headers=self.headers, params={"visibility": "all"})

        if response.status_code != 200:
            return f"GitHub API error {response.status_code}: {response.text}"

        repos = response.json()
        if not repos:
            return "You have no repositories."
        
        return "\n".join(f"- {repo['name']} ({'private' if repo['private'] else 'public'})" for repo in repos)

    def list_user_repos(self, username: str) -> str:
        url = f"{self.api_url}/users/{username}/repos"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            return f"GitHub API error {response.status_code}: {response.text}"

        repos = response.json()
        if not repos:
            return f"No public repositories found for user '{username}'."
        
        return "\n".join(f"- {repo['name']} ({'private' if repo['private'] else 'public'})" for repo in repos)

    def run(self, command: str) -> str:
        try:
            command = command.lower().strip()

            if command.startswith("list commits for repo"):
                parts = command.split("'")
                repo = parts[1]
                owner = parts[3]
                return self.get_recent_commits(owner, repo)

            elif command.startswith("list commits by user"):
                parts = command.split("'")
                username = parts[1]
                repo = parts[3]
                owner = parts[5]
                return self.get_commits_by_user(owner, repo, username)

            elif command.startswith("list my repos"):
                return self.list_my_repos()

            elif command.startswith("list repos for user"):
                parts = command.split("'")
                username = parts[1]
                return self.list_user_repos(username)

            else:
                return "❓ Sorry, I didn't understand that GitHub command."
        except Exception as e:
            return f"⚠️ GitHub Agent error: {e}"

if __name__ == "__main__":
    agent = GitHubAgent()
    print(agent.run("list commits by user 'torvalds' in repo 'linux' by owner 'torvalds'"))

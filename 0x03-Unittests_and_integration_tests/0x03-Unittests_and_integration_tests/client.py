import requests
from typing import Dict, List
from utils import get_json


class GithubOrgClient:
    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name: str):
        self.org_name = org_name

    def org(self) -> Dict:
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self) -> str:
        return self.org().get("repos_url")

    def public_repos(self, license: str = None) -> List[str]:
        repos = get_json(self._public_repos_url)
        repo_names = [repo["name"] for repo in repos]
        if license is None:
            return repo_names
        return [
            repo["name"]
            for repo in repos
            if repo.get("license", {}).get("key") == license
        ]

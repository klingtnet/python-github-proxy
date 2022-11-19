import logging
import sys
from typing import List
import os
from urllib.parse import urljoin

import requests

# Constants for common GitHub API HTTP headers.
# For details see: https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api#using-headers
GITHUB_TOKEN_KEY = "GITHUB_TOKEN"
GITHUB_ACCEPT = "application/vnd.github+json"


class GitHubClient:
    def __init__(
        self,
        token: str,
        logger: logging.Logger = None,
        base_url: str = "https://api.github.com",
    ):
        self.token = token
        self.logger = logger
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers = {
            "user-agent": "klingt.net/py-github",
            "Authorization": f"Bearer {token}",
        }

    def verify(self):
        """Verify that authenticated access works and the API is reachable."""
        resp = self.session.get(self._url("/user"), headers={"Accept": GITHUB_ACCEPT})
        resp.raise_for_status()
        body = resp.json()
        self._log(f"you're logged in as: {body.get('login')}")


    def _url(self, path: str) -> str:
        return urljoin(self.base_url, path)

    def _log(self, msg):
        if self.logger:
            self.logger.info(msg)


def main(args: List[str]):
    # Nothing will be logged if basic config wasn't called once.
    # Not the best logging API out there.
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    github_token = os.environ.get(GITHUB_TOKEN_KEY)
    if not github_token:
        log.critical(f"{GITHUB_TOKEN_KEY} required")

    gh = GitHubClient(github_token, logger=log)
    gh.verify()


if __name__ == "__main__":
    main(sys.argv[1:])

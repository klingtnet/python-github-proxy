from urllib.parse import urljoin
import logging

import requests

# Constants for common GitHub API HTTP headers.
# For details see: https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api#using-headers
GITHUB_ACCEPT = "application/vnd.github+json"


class GitHub:
    """A client for GitHub's REST API.
    For documentation of the API see https://docs.github.com/en/rest.
    """

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

    def starred(self, offset=1, page_size=50) -> (int, list[dict]):
        """Yield starred repositories."""

        while True:
            resp = self.session.get(
                self._url("/user/starred"),
                headers={"Accept": GITHUB_ACCEPT},
                params={"per_page": page_size, "page": offset},
            )
            resp.raise_for_status()
            page = resp.json()
            if len(page) < page_size:
                return 0, None

            yield offset, page
            offset += 1

    def _url(self, path: str) -> str:
        return urljoin(self.base_url, path)

    def _log(self, msg):
        if self.logger:
            self.logger.info(msg)

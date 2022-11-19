import logging
import sys
from typing import List
import os

import client


GITHUB_TOKEN_KEY = "GITHUB_TOKEN"


def main(args: List[str]):
    # Nothing will be logged if basic config wasn't called once.
    # Not the best logging API out there.
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    github_token = os.environ.get(GITHUB_TOKEN_KEY)
    if not github_token:
        log.critical(f"{GITHUB_TOKEN_KEY} required")

    gh = client.GitHub(github_token, logger=log)
    gh.verify()


if __name__ == "__main__":
    main(sys.argv[1:])

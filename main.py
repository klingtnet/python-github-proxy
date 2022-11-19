import argparse
import logging
import sys
from typing import List, Dict
import os

import client


GITHUB_TOKEN_KEY = "GITHUB_TOKEN"


def main(args: List[str], environ: Dict[str, str]):
    # Nothing will be logged if basic config wasn't called once.
    # Not the best logging API out there.
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    github_token = environ.get(GITHUB_TOKEN_KEY)
    if not github_token:
        log.critical(f"{GITHUB_TOKEN_KEY} required")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("--github-base-url", help=f"Base URL of GitHub REST API.")
    args = parser.parse_args(args)
    if args.github_base_url:
        gh = client.GitHub(github_token, logger=log, base_url=args.github_base_url)
    else:
        gh = client.GitHub(github_token, logger=log)

    gh.verify()

    # TODO: Implement server which exposes some client methods.


if __name__ == "__main__":
    main(sys.argv[1:], dict(os.environ))

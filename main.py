import argparse
import logging
import sys
from typing import List, Dict
import os

import client
import server


GITHUB_TOKEN_KEY = "GITHUB_TOKEN"


def main(argv: List[str], environ: Dict[str, str]):
    # Nothing will be logged if basic config wasn't called once.
    # Not the best logging API out there.
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    github_token = environ.get(GITHUB_TOKEN_KEY)
    if not github_token:
        log.critical(f"{GITHUB_TOKEN_KEY} required")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("--listen", default="127.0.0.1", help="address to listen on")
    parser.add_argument("--port", default=8899, help="port to listen on", type=int)
    parser.add_argument("--github-base-url", help="Base URL of GitHub REST API.")
    parser.add_argument("--development", help="development mode", action="store_true")
    args = parser.parse_args(argv)
    if args.github_base_url:
        gh = client.GitHub(github_token, logger=log, base_url=args.github_base_url)
    else:
        gh = client.GitHub(github_token, logger=log)

    app = server.new_app(log, gh)
    if args.development:
        # Note that app.run is not intended for production usage.
        app.run(host=args.listen, port=args.port)


if __name__ == "__main__":
    main(sys.argv[1:], dict(os.environ))

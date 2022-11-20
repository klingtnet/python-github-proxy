import logging

import requests
from flask import Flask, Response, request
import json
from client import GitHub


def new_app(log: logging.Logger, client: GitHub) -> Flask:
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def root():
        return {
            "routes": [
                app.url_for(endpoint, _external=True)
                for endpoint in ["health", "starred", "starred_stream"]
            ]
        }

    @app.route("/starred", methods=["GET"])
    def starred():
        params = {}
        if offset := request.args.get("offset"):
            params["offset"] = int(offset)
        if page_size := request.args.get("pageSize"):
            params["page_size"] = int(page_size)

        pages = []
        for page_no, page in client.starred(**params):
            log.info(f"/starred: fetching page {page_no}")
            pages += page
        return pages

    @app.route("/starred-stream", methods=["GET"])
    def starred_stream():
        params = {}
        if offset := request.args.get("offset"):
            params["offset"] = int(offset)
        if page_size := request.args.get("pageSize"):
            params["page_size"] = int(page_size)

        def generate():
            yield "["
            for page_no, page in client.starred(**params):
                if page_no > offset:
                    yield ","
                log.info(f"/starred: fetching page {page_no}")
                page_str = (
                    json.dumps(page, indent=2, sort_keys=True)
                    .removeprefix("[")
                    .removesuffix("]")
                )
                yield page_str
            yield "]"

        return Response(generate(), mimetype="application/json")

    @app.route("/health", methods=["GET"])
    def health():
        try:
            client.verify()
        except requests.HTTPError as e:
            return {"status": "unhealthy 😵", "error": str(e)}, 501
        return {"status": "healthy ❤️"}

    return app

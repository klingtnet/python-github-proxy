import pytest
import pytest_httpserver

import client


def test_client_stars_pagination(httpserver: pytest_httpserver.HTTPServer):
    httpserver.expect_ordered_request(
        "/user/starred",
        headers={
            "accept": client.GITHUB_ACCEPT,
            "authorization": "Bearer secret-token",
        },
        query_string={"per_page": "2", "page": "1"},
    ).respond_with_json([{"id": x} for x in range(2)])
    httpserver.expect_ordered_request(
        "/user/starred",
        headers={
            "accept": client.GITHUB_ACCEPT,
            "authorization": "Bearer secret-token",
        },
        query_string={"per_page": "2", "page": "2"},
    ).respond_with_json([{"id": 3}])

    cl = client.GitHub(token="secret-token", base_url=httpserver.url_for(""))
    pages = list(cl.starred(page_size=2))
    print(pages)

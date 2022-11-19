import pytest
import pytest_httpserver

import client
import main


def test_main_no_token():
    with pytest.raises(SystemExit):
        main.main(None, {})


def test_main_with_token(httpserver: pytest_httpserver.HTTPServer):
    handler = httpserver.expect_request(
        "/user",
        headers={
            "accept": client.GITHUB_ACCEPT,
            "authorization": "Bearer secret-token",
        },
    )
    handler.respond_with_json({"login": "klingtnet"})
    main.main(
        ["--github-base-url", httpserver.url_for("")],
        {main.GITHUB_TOKEN_KEY: "secret-token"},
    )

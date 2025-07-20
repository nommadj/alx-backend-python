TEST_PAYLOAD = [
    (
        {"repos_url": "https://api.github.com/orgs/google/repos"},
        [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3", "license": {"key": "apache-2.0"}},
        ],
        ["repo1", "repo2", "repo3"],
        ["repo3"],
    )
]

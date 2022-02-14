from utils import get_data_from_endpoint, parse_url_args
import requests

GH_ENDPOINTS = {
    "issues": "https://api.github.com/issues",
    "interactions": "https://api.github.com/user/interaction-limits",

}


class GitHub:
    def __init__(self, **config_options):
        self.__dict__.update(**config_options)
        self.session = requests.Session()
        if hasattr(self, 'api_token'):
            self.session.headers['Authorization'] = 'token %s' % self.api_token
        elif hasattr(self, 'username') and hasattr(self, 'password'):
            self.session.auth = (self.username, self.password)

    def get_issue_assigned_to_me(self, cache_dir=None, cache_time=3600, *args, **kwargs):
        endpoint, md5 = parse_url_args(GH_ENDPOINTS["issues"],
                                       *args,
                                       **kwargs)
        return get_data_from_endpoint(endpoint, f"github_issues_{md5}",
                                      headers=self.session.headers,
                                      cache_dir=cache_dir,
                                      cache_time=cache_time)

    def get_interactions(self, cache_dir=None, cache_time=3600, *args, **kwargs):
        endpoint, md5 = parse_url_args(GH_ENDPOINTS["interactions"],
                                       *args,
                                       **kwargs)
        return get_data_from_endpoint(endpoint, f"github_interactions_{md5}",
                                      headers=self.session.headers,
                                      cache_dir=cache_dir,
                                      cache_time=cache_time)

# def get_issues_assigned_to_me(token):
#     """
#     Get all issues assigned to me
#     """
#     endpoint = GH_ENDPOINTS["issues"]
#     params = parse_url_args(endpoint, {"assignee": "me"})
#     return get_data_from_endpoint(endpoint, token, params)


if __name__ == "__main__":
    import sys
    import json
    import os
    import requests
    import argparse

    github = GitHub(api_token="")
    issues = github.get_issue_assigned_to_me()
    print(json.dumps(issues, indent=4))

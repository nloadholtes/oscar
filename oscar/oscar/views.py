from pyramid.view import view_config
from pyramid import exceptions as exc
import requests

GITHUB_URL = 'https://api.github.com'


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'oscar'}


@view_config(route_name='checker', renderer='json')
def main_checker(request):
    github_data = _check_github(request)
    return github_data


def _check_github(request):
    username = request.params.get('username', None)
    if username is None:
        raise exc.HTTPBadRequest(body='Missing Username')
    repos = requests.get('{}/users/{}/repos'.format(GITHUB_URL, username)).json()
    output = []
    for repo in repos:
        name = repo['name']
        pulls_url = repo['pulls_url']
        pull_req = requests.get(pulls_url[:-9]).json()
        if len(pull_req) > 0:
            output.append(dict(name=name, url=repo['html_url'],
                                num_pulls=len(pull_req), pulls_url=pulls_url))
    print(output)
    # req = requests.get('{}/repos/{}/{}/pulls'.format(GITHUB_URL, username, repo))
    # prnm
    return output

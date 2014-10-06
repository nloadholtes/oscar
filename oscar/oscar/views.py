from pyramid.view import view_config
from pyramid import exceptions as exc
import requests

GITHUB_URL = 'https://api.github.com'
BITBUCKET_URL = 'https://bitbucket.org/api/2.0/repositories'


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'oscar'}


@view_config(route_name='checker', renderer='json')
def main_checker(request):
    username = request.params.get('username', None)
    if username is None:
        raise exc.HTTPBadRequest(body='Missing Username')
    github_data = _check_github(request)
    return github_data


def _check_github(username):
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
    return output


def _check_bitbucket(username):
    repos = requests.get('{}/{}'.format(BITBUCKET_URL, username)).json()
    output = []
    more_to_see = True
    while more_to_see:
        for repo in repos['values']:
            name = repo['name']
            pulls_url = repo['links']['pullrequests']['href']
            pull_req = requests.get(pulls_url).json()
            if len(pull_req['values']) > 0:
                output.append(dict(name=name, url=repo['links']['html'],
                                num_pulls=len(pull_req), pulls_url=pulls_url))
        # import pdb; pdb.set_trace()
        if repos.get('next', False):
            repos = requests.get(repos['next']).json()
        else:
            more_to_see = False
    print(output)
    return output

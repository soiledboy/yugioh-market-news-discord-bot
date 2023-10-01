import requests
username = 'tier1marketspace'
token = '37d1ea6c03d5dbe7b807e24243f1dc34786aef9d'
host = 'www.pythonanywhere.com'
id = '92730'

response = requests.post(
    'https://{host}/api/v0/user/{username}/always_on/{id}/restart/'.format(
        host=host, username=username, id = id
    ),
    headers={'Authorization': 'Token {token}'.format(token=token)}
)
if response.status_code == 200:
    print('CPU quota info:')
    print(response.content)
else:
    print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))

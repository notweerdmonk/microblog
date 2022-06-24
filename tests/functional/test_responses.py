import conftest
import base64
import json

#def test_index_anon_resp(test_client):
#    '''
#    GIVEN index.html page
#    WHEN GET request is made to the page by anonymous user
#    THEN check if response code is 302
#    '''
#    response = test_client.get('/index')
#    headers = dict(response.headers)
#
#    assert response.status_code == 302
#    assert 'Location' in headers.keys()
#    assert headers['Location'] == '/auth/login?next=%2Findex'
#
#def test_index_anon_redirect_resp(test_client):
#    '''
#    GIVEN index.html page
#    WHEN GET request is made to the page by anonymous user
#    THEN check if server redirects to login.html
#    '''
#    response = test_client.get('/index', follow_redirects=True)
#    body = str(response.data)
#
#    assert response.status_code == 200
#    assert len(response.history) == 1
#    assert response.request.path == '/auth/login'
#    assert 'Please log in to access this page.' in body
#
#def test_login_anon_resp(test_client):
#    '''
#    GIVEN login.html page
#    WHEN GET request is made to the page by anonymous user
#    THEN check if response code is 200
#    '''
#    response = test_client.get('/auth/login')
#
#    assert response.status_code == 200
#
#def test_logout_anon_resp(test_client):
#    '''
#    GIVEN logout.html page
#    WHEN GET request is made to the page by anonymous user
#    THEN check if response code is 302
#    '''
#    response = test_client.get('/auth/logout')
#    headers = dict(response.headers)
#
#    assert response.status_code == 302
#    assert 'Location' in headers.keys()
#    assert headers['Location'] == '/index'
#    
#def test_register_anon_resp(test_client):
#    '''
#    GIVEN register.html page
#    WHEN GET request is made to the page by anonymous user
#    THEN check if response code is 200
#    '''
#    response = test_client.get('/auth/register')
#
#    assert response.status_code == 200
#
#def test_user_anon_resp(test_client):
#    '''
#    GIVEN user.html page
#    WHEN GET request is made to the page by anonymous user
#    THEN check if response code is 404
#    '''
#    response = test_client.get('/user/')
#
#    assert response.status_code == 404
#
#def test_edit_profile_anon_resp(test_client):
#    '''
#    GIVEN edit_profile.html page
#    WHEN GET request is made to the page by anonymous user
#    THEN check if response code is 302
#    '''
#    response = test_client.get('/edit_profile')
#    headers = dict(response.headers)
#
#    assert 'Location' in headers.keys()
#    assert headers['Location'] == '/auth/login?next=%2Fedit_profile'
#
#    assert response.status_code == 302
#
#def test_explore_anon_resp(test_client):
#    '''
#    GIVEN explore.html page
#    WHEN GET request is made to the page by anonymous user
#    THEN check if response code is 302
#    '''
#    response = test_client.get('/explore')
#    headers = dict(response.headers)
#
#    assert response.status_code == 302
#    assert 'Location' in headers.keys()
#    assert headers['Location'] == '/auth/login?next=%2Fexplore'
#
#def test_login_valid_auth_resp(test_client, request_context, add_new_user):
#    '''
#    GIVEN login.html page
#    WHEN POST request is made with valid credentials
#    THEN check if login is successful
#    '''
#    session, csrf_token = request_context
#    response = test_client.post('/auth/login',
#            data={'csrf_token': csrf_token,
#                  'username': 'Rahul',
#                  'password': 'password'})
#    headers = dict(response.headers)
#
#    assert response.status_code == 302
#    assert 'Location' in headers.keys()
#    assert headers['Location'] == '/index'
#
#def test_api_auth_token_resp(test_client, add_new_user):
#    '''
#    GIVEN /api/tokens route
#    WHEN GET request is made
#    THEN check if response code is 405 (method not allowed)
#    '''
#    response = test_client.get('/api/tokens')
#
#    assert response.status_code == 405
#
#    '''
#    GIVEN /api/tokens route
#    WHEN POST request is made with invalid credentials
#    THEN check if response code is 401 (unauthorized)
#    '''
#    credentials = base64.b64encode(b'foo:bar').decode('utf-8')
#    response = test_client.post('/api/tokens',
#            headers={'Authorization': 'Basic ' + credentials})
#
#    assert response.status_code == 401
#    assert response.is_json == True
#    assert 'error' in response.json
#    assert response.json['error'] == 'Unauthorized'
#
#    '''
#    GIVEN /api/tokens route
#    WHEN POST request is made with valid credentials
#    THEN check if authorization token is returned
#    '''
#    credentials = base64.b64encode(b'Rahul:password').decode('utf-8')
#    response = test_client.post('/api/tokens',
#            headers={'Authorization': 'Basic ' + credentials})
#
#    assert response.status_code == 200
#    assert response.is_json == True
#    assert 'token' in response.json
#
#    token = response.json['token']
#
#    '''
#    GIVEN /api/tokens route
#    WHEN DELETE request is made with invalid token
#    THEN check if response code is 401 (unauthorized)
#    '''
#    response = test_client.delete('/api/tokens',
#            headers={'Authorization': 'Bearer foobar'})
#
#    assert response.status_code == 401
#    assert response.is_json == True
#    assert 'error' in response.json
#    assert response.json['error'] == 'Unauthorized'
#
#    '''
#    GIVEN /api/tokens route
#    WHEN DELETE request is made with valid token
#    THEN check if response code is 204 (no content)
#    '''
#    response = test_client.delete('/api/tokens',
#            headers={'Authorization': 'Bearer ' + token})
#
#    assert response.status_code == 204

import conftest

def test_index_anon_resp(test_client):
    '''
    GIVEN index.html page
    WHEN GET request is made to the page by anonymous user
    THEN check if response code is 302
    '''
    response = test_client.get('/index')
    headers = dict(response.headers)

    assert response.status_code == 302
    assert 'Location' in headers.keys()
    assert headers['Location'] == '/auth/login?next=%2Findex'

def test_login_anon_resp(test_client):
    '''
    GIVEN login.html page
    WHEN GET request is made to the page by anonymous user
    THEN check if response code is 200
    '''
    response = test_client.get('/auth/login')

    assert response.status_code == 200

def test_logout_anon_resp(test_client):
    '''
    GIVEN logout.html page
    WHEN GET request is made to the page by anonymous user
    THEN check if response code is 302
    '''
    response = test_client.get('/auth/logout')
    headers = dict(response.headers)

    assert response.status_code == 302
    assert 'Location' in headers.keys()
    assert headers['Location'] == '/index'
    
def test_register_anon_resp(test_client):
    '''
    GIVEN register.html page
    WHEN GET request is made to the page by anonymous user
    THEN check if response code is 200
    '''
    response = test_client.get('/auth/register')

    assert response.status_code == 200

def test_user_anon_resp(test_client):
    '''
    GIVEN user.html page
    WHEN GET request is made to the page by anonymous user
    THEN check if response code is 404
    '''
    response = test_client.get('/user/')

    assert response.status_code == 404

def test_edit_profile_anon_resp(test_client):
    '''
    GIVEN edit_profile.html page
    WHEN GET request is made to the page by anonymous user
    THEN check if response code is 302
    '''
    response = test_client.get('/edit_profile')
    headers = dict(response.headers)

    assert 'Location' in headers.keys()
    assert headers['Location'] == '/auth/login?next=%2Fedit_profile'

    assert response.status_code == 302

def test_explore_anon_resp(test_client):
    '''
    GIVEN explore.html page
    WHEN GET request is made to the page by anonymous user
    THEN check if response code is 302
    '''
    response = test_client.get('/explore')
    headers = dict(response.headers)

    assert response.status_code == 302
    assert 'Location' in headers.keys()
    assert headers['Location'] == '/auth/login?next=%2Fexplore'

def test_login_valid_auth_response(test_client, request_context, add_new_user):
    '''
    GIVEN login.html page
    WHEN POST request is made with valid credentials
    THEN check if login is successful
    '''
    session, csrf_token = request_context
    response = test_client.post('/auth/login',
            data={'csrf_token': csrf_token,
                  'username': 'Rahul',
                  'password': 'password'})
    headers = dict(response.headers)

    assert response.status_code == 302
    assert 'Location' in headers.keys()
    assert headers['Location'] == '/index'

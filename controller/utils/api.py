from auth0.v3.authentication import GetToken
import openlattice
import requests
import os

def get_jwt():
    domain='openlattice.auth0.com'
    realm='Username-Password-Authentication'
    scope='openid email nickname roles user_id organizations'
    audience='https://api.openlattice.com'
    client_id='o8Y2U2zb5Iwo01jdxMN1W2aiN8PxwVjh'
    username = os.environ.get("bamboo_EDM_USERNAME")
    password = os.environ.get("bamboo_EDM_PASSWORD")
    get_token = GetToken(domain)
    token = get_token.login(client_id=client_id,
        client_secret="", username=username, password=password,
        scope=scope, realm=realm, audience=audience,
        grant_type='http://auth0.com/oauth/grant-type/password-realm')
    return token

def get_api_instance(baseurl, jwt):
    configuration = openlattice.Configuration()
    configuration.host = baseurl
    configuration.api_key_prefix['Authorization'] = 'Bearer'
    configuration.api_key['Authorization'] = jwt
    api_instance = openlattice.ApiClient(configuration)
    return api_instance

def request_edm(baseurl, jwt):
    headers = {"Authorization":"Bearer %s"%jwt}
    url = os.path.join(baseurl,"datastore/edm/")
    edm = requests.get(url,headers=headers)
    return edm.json()


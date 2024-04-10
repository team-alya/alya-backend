import os
import swiftclient
from dotenv import load_dotenv


load_dotenv()

_authurl = os.getenv('OS_AUTH_URL')
_auth_version = os.getenv('OS_IDENTITY_API_VERSION')
_user = os.getenv('OS_USERNAME')
_key = os.getenv('OS_PASSWORD')
_os_options = {
    'user_domain_name': os.getenv('OS_USER_DOMAIN_NAME'),
    'project_domain_name': os.getenv('OS_USER_DOMAIN_NAME'),
    'project_name': os.getenv('OS_PROJECT_NAME')
}

conn = swiftclient.Connection(
    authurl=_authurl,
    user=_user,
    key=_key,
    os_options=_os_options,
    auth_version=_auth_version
)
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
import logging
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()
logger = logging.getLogger(__name__)

@database_sync_to_async
def get_user_from_token(token_key):
    try:
        token = AccessToken(token_key)
        user_id = token.payload['user_id']
        return User.objects.get(pk=user_id)
    except Exception as e:
        logger.error(f"Error retrieving user from token: {str(e)}")
        return AnonymousUser()

@database_sync_to_async
def get_user_from_session(session_key):
    try:
        session = Session.objects.get(session_key=session_key)
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        if user_id:
            return User.objects.get(pk=user_id)
    except Exception as e:
        logger.error(f"Error retrieving user from session: {str(e)}")
    return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        # Log headers to verify what cookies are being sent in production
        for header in scope.get('headers', []):
            logger.info(f"Header: {header}")

        # Get cookies from the headers
        cookies_header = dict(scope.get('headers', []))
        cookie_string = cookies_header.get(b'cookie', b'').decode('utf-8')

        # Log the raw cookie string
        logger.info(f"Raw cookie string: {cookie_string}")

        # Parse cookies
        try:
            cookies = {item.split('=')[0].strip(): item.split('=')[1].strip() for item in cookie_string.split(';') if '=' in item}
            logger.info(f"Parsed cookies: {cookies}")
        except Exception as e:
            logger.error(f"Error parsing cookies: {str(e)}")
            cookies = {}

        # Extract sessionid or authtoken from cookies
        session_key = cookies.get('sessionid', None)
        token_key = cookies.get('authtoken', None)

        # Log the session and token keys
        logger.info(f"Session key: {session_key}, Token key: {token_key}")

        # Check for sessionid or token and assign user
        if session_key:
            scope['user'] = await get_user_from_session(session_key)
            logger.info(f"User authenticated from session: {scope['user']}")
        elif token_key:
            scope['user'] = await get_user_from_token(token_key)
            logger.info(f"User authenticated from token: {scope['user']}")
        else:
            scope['user'] = AnonymousUser()
            logger.warning("AnonymousUser assigned due to missing sessionid or token.")

        return await super().__call__(scope, receive, send)

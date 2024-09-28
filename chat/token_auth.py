from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from useraccount.models import User
import logging

logger = logging.getLogger(__name__)

@database_sync_to_async
def get_user(token_key):
    try:
        # Validate token and return user
        token = AccessToken(token_key)
        user_id = token.payload['user_id']
        return User.objects.get(pk=user_id)
    except Exception as e:
        logger.error(f"Error retrieving user: {str(e)}")
        return AnonymousUser()  # Return AnonymousUser if there is an error

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
    # Decode query string to get token
        query_string = scope['query_string'].decode()
        query = dict((x.split('=') for x in query_string.split('&') if '=' in x))

        # Get token from query
        token_key = query.get('token', None)

        # Validate token if present
        if token_key:
            scope['user'] = await get_user(token_key)
        else:
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)

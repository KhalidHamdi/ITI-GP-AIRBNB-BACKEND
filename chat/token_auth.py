from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from useraccount.models import User

# @database_sync_to_async
# def  get_user(token_key):
#     try:
#         token=AccessToken(token_key)
#         user_id = token.payload['user_id']
#         return User.objects.get(pk=user_id)
#     except Exception as e:
#         return AnonymousUser

# class TokenAuthMiddleware(BaseMiddleware):
#     def __init__(self, inner):
#         self.inner=inner
#     async def __call__(self, scope,recive,send):
#         query=dict((x.split('=')for x in scope['query_string'].decode().split('&')))
#         token_key=query.get('token')
#         scope['user']=await get_user(token_key)
#         return await super().__call__(scope,recive,send)

@database_sync_to_async
def get_user(token_key):
    try:
        # Normally validate token and return user
        token = AccessToken(token_key)
        user_id = token.payload['user_id']
        return User.objects.get(pk=user_id)
    except Exception as e:
        # If token is invalid or missing, return AnonymousUser
        return AnonymousUser

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Decode query string to get token (comment out to bypass token check)
        query = dict((x.split('=') for x in scope['query_string'].decode().split('&')))
        
        # Uncomment this to allow requests without token
        token_key = query.get('token', None)

        # If token is found, validate it, else use AnonymousUser
        if token_key:
            scope['user'] = await get_user(token_key)
        else:
            # If no token is present, use AnonymousUser for now
            scope['user'] = AnonymousUser()
        
        return await super().__call__(scope, receive, send)
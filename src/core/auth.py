import jwt
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from users.models import User
from django.conf import settings

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('next-auth.session-token')
        if not token:
            return None

        try:
            decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_payload.get('sub')
            user = User.objects.get(pk=user_id)
            return (user, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except jwt.DecodeError as e:
            raise AuthenticationFailed('Token is invalid.')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found.')

    def authenticate_header(self, request):
        return 'Bearer'
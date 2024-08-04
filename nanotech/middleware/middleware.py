from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse, HttpResponse

class CheckBlacklistedTokenMiddleware(MiddlewareMixin):
    pass
    # def process_request(self, request):
    #     jwt_authenticator = JWTAuthentication()
    #     auth_header = request.headers.get('Authorization')

    #     if auth_header is None:
    #         return

    #     try:
    #         # Extract token from the Authorization header
    #         token = auth_header.split(' ')[1]
    #         # print(token, '-----------')
    #         validated_token = jwt_authenticator.get_validated_token(token)
    #         # print(validated_token, '-----------')
    #         user = jwt_authenticator.get_user(validated_token)
    #         print(user, '-----------')

    #         header_token = token.split('.')[0]
    #         # print(header_token, '-----------')
            
    #         # # Check if the access token is blacklisted
    #         jti = validated_token.get('jti')
    #         # print(jti, '-----------')
    #         if jti:
    #             print(jti, '-----------')
    #         #     token = OutstandingToken.objects.get(jti=jti)
    #         #     # print(token, '-----------')
    #         #     if BlacklistedToken.objects.filter(token=token).exists():
    #         #         raise InvalidToken("Token is blacklisted")
    #     except (InvalidToken, TokenError, Exception) as e:
    #         return JsonResponse({"detail": str(e)}, status=401)
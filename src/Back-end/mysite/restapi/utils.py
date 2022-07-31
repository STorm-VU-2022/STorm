from datetime import timedelta

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    access_token.set_exp(lifetime=timedelta(days=1))
    return {
        #'refresh': str(refresh),
        'access': str(access_token),
        'full_name': user.full_name
    }

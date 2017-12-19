from django.contrib.auth import get_user_model

User = get_user_model()


def get_sentinel_user():
    return User.objects.get_or_create(
        email='sentinel@gmail.com',
        first_name='deleted',
        last_name='sentinel',
    )

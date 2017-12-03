from django.conf.urls import url

from ..apis import SignUp, LogIn, EmailIsUnique, ProfileRetrieveUpdateDelete, ProfileImage

urlpatterns = [
    url(r'sign-up/$', SignUp.as_view(), name='sign-up'),
    url(r'log-in/$', LogIn.as_view(), name='log-in'),
    url(r'email-check/$', EmailIsUnique.as_view(), name='email-check'),
    url(r'profile/(?P<pk>\d+)/$', ProfileRetrieveUpdateDelete.as_view(), name='profile-detail'),
    url(r'profile/(?P<profile_pk>\d+)/image/$', ProfileImage.as_view(), name='profile-image'),
]

from django.conf.urls import url

from ..apis import SignUp, LogIn, EmailIsUnique, ProfileRetrieveUpdate, ProfileImageCreate, \
    ProfileImageRetrieveUpdateDelete

urlpatterns = [
    url(r'sign-up/$', SignUp.as_view(), name='sign-up'),
    url(r'log-in/$', LogIn.as_view(), name='log-in'),
    url(r'email-check/$', EmailIsUnique.as_view(), name='email-check'),
    url(r'profile/(?P<pk>\d+)/$', ProfileRetrieveUpdate.as_view(), name='profile-detail'),
    url(r'profile/(?P<pk>\d+)/image/$', ProfileImageCreate.as_view(), name='profile-image'),
    url(r'profile/(?P<profile_pk>\d+)/image/(?P<pk>\d+)/$', ProfileImageRetrieveUpdateDelete.as_view(),
        name='profile-image-detail'),
]


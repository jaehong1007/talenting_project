from django.conf.urls import url

from ..apis import SignUp, LogIn, EmailIsUnique, ProfileRetrieveUpdate, ProfileImageCreate, \
    ProfileImageRetrieveUpdateDelete, GuestReviewCreate, WishListRetrieve, HostingWishListDelete, EventWishListDelete, \
    PasswordMissing, PasswordReset

urlpatterns = [
    url(r'sign-up/$', SignUp.as_view(), name='sign-up'),
    url(r'log-in/$', LogIn.as_view(), name='log-in'),
    url(r'email-check/$', EmailIsUnique.as_view(), name='email-check'),
    url(r'password-missing/$', PasswordMissing.as_view(), name='password-missing'),
    url(r'password-reset/$', PasswordReset.as_view(), name='password-reset'),
    url(r'profile/(?P<pk>\d+)/$', ProfileRetrieveUpdate.as_view(), name='profile-detail'),
    url(r'profile/(?P<pk>\d+)/image/$', ProfileImageCreate.as_view(), name='profile-image'),
    url(r'profile/(?P<profile_pk>\d+)/image/(?P<pk>\d+)/$', ProfileImageRetrieveUpdateDelete.as_view(),
        name='profile-image-detail'),
    url(r'profile/(?P<pk>\d+)/review/$', GuestReviewCreate.as_view(), name='profile-review'),
    url(r'profile/(?P<pk>\d+)/wish-list/$', WishListRetrieve.as_view(), name='wish-list'),
    url(r'profile/(?P<pk>\d+)/wish-list/hosting-delete/(?P<hosting_pk>\d+)/$', HostingWishListDelete.as_view(),
        name='wish-list-host-delete'),
    url(r'profile/(?P<pk>\d+)/wish-list/event-delete/(?P<event_pk>\d+)/$', EventWishListDelete.as_view(),
        name='wish-list-host-delete'),
]

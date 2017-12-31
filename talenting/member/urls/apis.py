from django.conf.urls import url

from ..apis import SignUp, LogIn, EmailIsUnique, ProfileRetrieveUpdate, ProfileImageCreate, \
    ProfileImageRetrieveUpdateDelete, GuestReviewListCreate, WishListRetrieve, HostingWishListDelete, \
    EventWishListDelete, \
    PasswordMissing, PasswordReset, EventParticipateList, ProfileWishListDelete, WishListProfileToggle, \
    MyTripListCreateView, MyTripRetrieveUpdateDeleteView, SignOut, MyTripCreatedList, MyTripCreatedListBy

urlpatterns = [
    # 유저 인증
    url(r'^sign-up/$', SignUp.as_view(), name='sign-up'),
    url(r'^log-in/$', LogIn.as_view(), name='log-in'),
    url(r'^email-check/$', EmailIsUnique.as_view(), name='email-check'),
    url(r'^password-missing/$', PasswordMissing.as_view(), name='password-missing'),
    url(r'^password-reset/$', PasswordReset.as_view(), name='password-reset'),
    url(r'^sign-out/$', SignOut.as_view(), name='sign-out'),
    # 프로필 관리
    url(r'^profile/(?P<pk>\d+)/$', ProfileRetrieveUpdate.as_view(), name='profile-detail'),
    url(r'^profile/(?P<pk>\d+)/image/$', ProfileImageCreate.as_view(), name='profile-image'),
    url(r'^profile/(?P<profile_pk>\d+)/image/(?P<pk>\d+)/$', ProfileImageRetrieveUpdateDelete.as_view(),
        name='profile-image-detail'),
    # 개인 리뷰 관리
    url(r'^profile/(?P<pk>\d+)/review/$', GuestReviewListCreate.as_view(), name='profile-review'),
    # 위시리스트 관리
    url(r'^profile/(?P<pk>\d+)/wish-list/$', WishListRetrieve.as_view(), name='wish-list'),
    url(r'^profile/(?P<pk>\d+)/wish-list/hosting-delete/(?P<hosting_pk>\d+)/$', HostingWishListDelete.as_view(),
        name='wish-list-host-delete'),
    url(r'^profile/(?P<pk>\d+)/wish-list/event-delete/(?P<event_pk>\d+)/$', EventWishListDelete.as_view(),
        name='wish-list-host-delete'),
    url(r'^profile/(?P<pk>\d+)/wish-list/profile-delete/(?P<profile_pk>\d+)/$', ProfileWishListDelete.as_view(),
        name='wish-list-host-delete'),
    url(r'^profile/(?P<pk>\d+)/wish-list-toggle/$', WishListProfileToggle.as_view(), name='wish-list-add'),
    # 내가 참여한 이벤트 보기
    url(r'^profile/(?P<pk>\d+)/my-event/$', EventParticipateList.as_view(),
        name='event-participate-list'),
    # 여행 등록
    url(r'mytrip/$', MyTripListCreateView.as_view(), name='mytrip-list'),
    url(r'mytrip/(?P<mytrip_pk>\d+)/$', MyTripRetrieveUpdateDeleteView.as_view(), name='mytrip-detail'),
    url(r'mytrip/created/$', MyTripCreatedList.as_view(), name='mytrip-created'),
    url(r'mytrip/created/(?P<pk>\d+)/$', MyTripCreatedListBy.as_view(), name='mytrip-created-by')
]

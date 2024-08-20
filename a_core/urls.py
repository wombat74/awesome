from django.contrib import admin
from django.urls import path, include
from a_posts.views import *
from a_users.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', home_view, name='home'),
    path('category/<tag>/', home_view, name='category'),
    path('post/create/', post_create_view, name='post-create'),
    path('post/delete/<pk>/', post_delete_view, name='post-delete'),
    path('post/edit/<pk>/', post_edit_view, name='post-edit'),
    path('post/<pk>/', post_page_view, name='post'),
    path('profile/', profile_view, name='profile'),
    path('<username>/', profile_view, name='userprofile'),
    path('profile/edit/', profile_edit_view, name='profile-edit'),
    path('profile/delete/', profile_delete_view, name='profile-delete'),
    path('profile/onboarding/', profile_edit_view, name="profile-onboarding"),
    path('commentsent/<pk>', comment_sent, name="comment-sent"),
    path('comment/delete/<pk>', comment_delete_view, name="comment-delete"),
    path('reply-sent/<pk>', reply_sent, name="reply-sent"),
    path('reply/delete/<pk>', reply_delete_view, name="reply-delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

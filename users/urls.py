from django.urls import path
from .views import *


urlpatterns = [
    path('registrations/new/', registrations, name="sign-up"),
    path('registrations/new/verification',
         mail_verification, name="verification"),
    path('registrations/new/verification/verify',
         getVerified, name="get-verified"),
    path('login/', userlogin, name="login"),
    path('login/forgot-password', forgotPassword, name="forgot-password"),
    path('login/password-reset-done',
         password_reset_done, name="password_reset_done"),
    path('login/password-reset-confirm/<uid>/<token>',
         password_reset_confirm, name="password-reset-confirm"),
    path('login/password-reset-complete',
         password_reset_complete, name="password-reset-complete"),
    path('login/password-reset-failed',
         password_reset_link_invalid, name="password-reset-failed"),
    path('account/profile', my_profile, name="my-profile"),
    path('account/profile/add-picture-profile',
         add_picture_profile, name="add-picture-profile"),
    path('account/password', user_change_password, name="change-password"),
    path('account/articals/add/artical', write_article, name="write-article"),
    path('account/articals/<artical_title>/edit/artical',
         edit_article, name="edit-article"),
    path('account/articals', my_articals, name="my-articals"),
    path('account/favorites', my_favorites, name="my-favorites"),
    path('add-to-favorites/<int:item_id>/',
         add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<int:item_id>/',
         remove_from_favorites, name='remove_from_favorites'),


    path('logout/', userlogout, name="logout"),
]

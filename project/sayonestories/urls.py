from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('userregform', views.userregisterform, name='userregister'),
    path('validateregister',views.validate_register, name='validate_register'),
    path('userprofile',views.User_profile_page,name='user_profile_page'),
    path('addstorypage',views.add_story_page,name='add_story_page'),
    path('substory',views.add_sub_story,name='add_sub_story'),
    path('addstory',views.add_story,name='add_story'),
    path('addblog',views.add_blog, name='add_blog'),
    path('basicupload/<int:id>/',views.basicupload,name='basic_upload'),
    path('upload',views.uploadpic,name='upload_page'),
    path('clear',views.clear_database,name='clear_images'),
    path('userstorypage',views.user_stories_page,name='user_stories_page'),
    path('storydetail/<int:id>/',views.story_detail_page,name='story_detail_page'),

]

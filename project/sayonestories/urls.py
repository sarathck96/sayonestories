from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('userregform', views.userregisterform, name='userregister'),
    path('validateregister',views.validate_register, name='validate_register'),
    path('userhome',views.User_home_page,name='user_home_page'),
    path('addstorypage',views.add_story_page,name='add_story_page'),
    path('substory',views.add_sub_story,name='add_sub_story'),
    path('addstory',views.add_story,name='add_story'),
    path('addblog',views.add_blog, name='add_blog'),
    path('basicupload/<int:id>/',views.basicupload,name='basic_upload'),
    path('upload',views.uploadpic,name='upload_page'),
    path('clear',views.clear_database,name='clear_images'),
    path('userstorypage',views.user_stories_page,name='user_stories_page'),
    path('storydetail/<int:id>/',views.story_detail_page,name='story_detail_page'),
    path('delete_story/<int:story_id>/',views.delete_story,name='delete_story'),
    path('userprofilepage',views.user_profile_page,name='user_profile_page'),
    path('updateprofilepic',views.update_profile_pic, name='update_profile_pic'),
    path('like_story/<int:story_id>/',views.like_story, name='like_story'),

    path('test',views.testupload,name='test_upload'),
    path('testvalidate' ,views.testvalidate,name='test_validate'),



]

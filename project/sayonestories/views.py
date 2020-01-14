from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext
from django.views import View
from django.core.mail import EmailMessage
from .forms import UserRegistrationform, StoryAddForm, AddBlog, PhotoForm
from django.forms import ValidationError, forms
from django.contrib.auth.models import User
from .models import Story, Blog, Images ,Sayoneuser


# Create your views here.

def home(request):
    return render(request, 'sayonestories/home.html', context={})


def userregisterform(request):
    form = UserRegistrationform()
    return render(request, 'sayonestories/userregistration.html', context={'form': form})


def validate_register(request):
    if request.method == 'POST':
        form = UserRegistrationform(request.POST, request.FILES)
        if form.is_valid():
            sayone = form.save(commit=False)
            userObj = form.cleaned_data
            username = userObj['username']
            email = userObj['mailid']
            password = userObj['password']
            cnf_password = userObj['cnf_pass']

            error_codes = []
            if User.objects.filter(email=email).exists():
                error_codes.append('email_exists')
            elif User.objects.filter(username=username).exists():
                error_codes.append('username_exists')
            elif password != cnf_password:
                error_codes.append('passwords_nomatch')

            print("///", error_codes)

            if 'email_exists' in error_codes:
                form.errors['mailid'] = form.error_class(['Mail ID already in use'])

            elif 'username_exists' in error_codes:
                form.errors['username'] = form.error_class(['username already taken'])
            elif 'passwords_nomatch' in error_codes:
                form.errors['password'] = form.error_class(['passwords did not match'])

            if len(error_codes) == 0:
                sayoneuser = User.objects.create_user(username=username, email=email, password=password)
                sayone.user = sayoneuser
                sayone.save()
                return redirect('home')
            else:
                return render(request, 'sayonestories/userregistration.html', context={'form': form})



    else:
        form = UserRegistrationform()

    return render(request, 'sayonestories/userregistration.html', {'form': form})


def User_home_page(request):
    pic_url = request.user.sayone_user.profile_pic
    story_object_for_user = Story.objects.filter(story_user=request.user)

    all_story_objects = Story.objects.all().order_by('-date_created')

    return render(request, 'sayonestories/UserHome.html', context={'img_url': pic_url,'stories':all_story_objects})


def add_story_page(request):
    form = StoryAddForm()

    return render(request, 'sayonestories/addstory.html', context={'form': form})


def add_story(request):
    if request.method == 'POST':
        form = StoryAddForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            print('/////', request.user)
            profile.story_user = request.user
            profile.story_author = request.user.sayone_user.name

            profile.save()
            return redirect('add_sub_story')
        else:
            return render(request, 'sayonestories/addstory.html', context={'form': form})
    else:
        form = StoryAddForm()
        render(request, 'sayonestories/addstory.html', context={'form': form})


def add_sub_story(request):
    story_object = Story.objects.latest('story_id')

    if story_object.story_type in [0, 1]:
        form1 = AddBlog()
        return render(request, 'sayonestories/addstory.html', context={'story': story_object, 'form1': form1})
    else:
        return render(request, 'sayonestories/addstory.html', context={'story': story_object, 'form2': 'picgallery'})


def add_blog(request):
    print('call here')
    story_id = request.POST.get('storyid')
    story_obj = Story.objects.filter(story_id=story_id)
    print('ssss', story_obj)

    if request.method == 'POST':
        form = AddBlog(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.story = story_obj[0]
            blog.save()
            return render(request, 'sayonestories/Loginpage.html', context={})
        else:
            return render(request, 'sayonestories/addstory.html', context={})
    else:
        return render(request, 'sayonestories/addstory.html', context={})


def basicupload(request, id):
    story_id = id
    story_obj = Story.objects.filter(story_id=story_id)
    form = PhotoForm(request.POST, request.FILES)
    if form.is_valid():
        photo = form.save(commit=False)
        photo.story = story_obj[0]
        photo.save()
        data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
    else:
        data = {'is_valid': False}
    return JsonResponse(data)


def uploadpic(request):
    photos_list = Images.objects.all()
    return render(request, 'sayonestories/uploadpics.html', {'photos': photos_list})


def clear_database(request):
    for photo in Images.objects.all():
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))


def user_stories_page(request):
    story_objects_for_user = Story.objects.filter(story_user=request.user)
    return render(request, 'sayonestories/userstories_page.html', context={'stories': story_objects_for_user})


def story_detail_page(request, id):
    story_obj = Story.objects.filter(story_id=id)[0]

    if story_obj.story_type in [0, 1]:
        for item in story_obj.blog_story.all():
            pic_url = item.blog_pic
            blog_description = item.blog_description

        context = {'blog': 'blog', 'picurl': pic_url, 'description': blog_description, 'story': story_obj}
        return render(request, 'sayonestories/story_detail_page.html', context)
    else:
        sub_story_object = story_obj.image_story.all()

        count = story_obj.image_story.count()

        data_slide = []

        for i in range(0, count):
            data_slide.append(i)

        for item in sub_story_object:
            print(item.file)
        context1 = {'substory': sub_story_object, 'story': story_obj}
        return render(request, 'sayonestories/story_detail_page.html', context=context1)


def delete_story(request,story_id):
    item = Story.objects.get(story_id=story_id)
    item.delete()
    messages.success(request, ("Story has been deleted"))
    return redirect(user_stories_page)


def user_profile_page(request):
    profile_details = {}
    name = request.user.sayone_user.name
    mailid = request.user.sayone_user.mailid
    username = request.user.sayone_user.username
    profile_pic = request.user.sayone_user.profile_pic

    stories = Story.objects.filter(story_user=request.user)
    story_count = stories.count()

    profile_details = {'name':name,'mailid':mailid,'username':username,'profile_pic':profile_pic,'story_count':story_count}

    print('kkk',profile_details)
    return render(request,'sayonestories/UserProfile.html',context={'profile_details':profile_details})


def update_profile_pic(request):
    print('test',request.FILES['pic'])
    obj = Sayoneuser.objects.get(user=request.user)
    obj.profile_pic = request.FILES['pic']
    obj.save()
    return redirect(user_profile_page)
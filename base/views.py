from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Blog, Topic, Message, User
from .forms import BlogForm, UserForm, MyUserCreationForm


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            # messages.error(request, 'Error occured during registration')
            return render(request, 'base/login_register.html', {'form':form})

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    blogs = Blog.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    blog_count = blogs.count()
    blog_messages = Message.objects.filter(
        Q(blog__topic__name__icontains=q))[0:3]

    context = {'blogs': blogs, 'topics': topics,
               'blog_count': blog_count, 'blog_messages': blog_messages}
    return render(request, 'base/home.html', context)


def blog(request, pk):
    blog = Blog.objects.get(id=pk)
    blog_messages = blog.message_set.all()
    participants = blog.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            blog=blog,
            body=request.POST.get('body')
        )
        blog.participants.add(request.user)
        return redirect('blog', pk=blog.id)

    context = {'blog': blog, 'blog_messages': blog_messages,
               'participants': participants}
    return render(request, 'base/blog.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    blogs = user.blog_set.all()
    blog_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'blogs': blogs,
               'blog_messages': blog_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createBlog(request):
    form = BlogForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Blog.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/blog_form.html', context)


@login_required(login_url='login')
def updateBlog(request, pk):
    blog = Blog.objects.get(id=pk)
    form = BlogForm(instance=blog)
    topics = Topic.objects.all()
    if request.user != blog.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        blog.name = request.POST.get('name')
        blog.topic = topic
        blog.description = request.POST.get('description')
        blog.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'blog': blog}
    return render(request, 'base/blog_form.html', context)


@login_required(login_url='login')
def deleteBlog(request, pk):
    blog = Blog.objects.get(id=pk)

    if request.user != blog.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        blog.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': blog})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    blog_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'blog_messages': blog_messages})

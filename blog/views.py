from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, Coinshakhzot, Profile, Follow
from django.contrib import messages
from .forms import ProfileForm, PostForm
from django.http import HttpResponse, HttpResponseForbidden
from django.db.utils import IntegrityError
# Create your views here.
def helloword(request):
	return HttpResponse('Hello, Братишка')

@login_required
def post_list(request):
    post = Post.objects.all().order_by('-created_at')
    users = User.objects.all()
    user = request.user
    return render(request, 'post_list.html', {'posts': post, 'users': users, 'user':user})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    referer = request.META.get('HTTP_REFERER')
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # убираем лайк
    else:
        post.likes.add(request.user)     # ставим лайк
    return redirect(referer, post_id=post.id)

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        text = request.POST.get("text")
        if text.strip():
            Comment.objects.create(author=request.user, post=post, text=text)
    return redirect('post_detail', post_id=post.id)


def defshakhzot(request):
    post = Post.objects.all()
    user = request.user
    index, created = Coinshakhzot.objects.get_or_create(id=1)
    return render(request, 'shakhzot.html', {
        'user': user,
        'index': index
    })


def add(request):
    index, created = Coinshakhzot.objects.get_or_create(id=1)
    index.coin += 1
    index.save()
    return redirect('shakhzot')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Пароли не совпадают!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Такой пользователь уже существует!')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        Profile.objects.create(user=user)
        messages.success(request, 'Регистрация успешна! Теперь войдите.')
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            messages.error(request, 'Неверное имя пользователя или пароль!')
            return redirect('login')
        messages.success(request, 'Вход успешен! Вы вошли.')
        return redirect('post_list')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request, username):
    user = request.user
    profile_user = get_object_or_404(User, username=username)
    profile = profile_user.profile 
    posts = Post.objects.all().filter(author=profile_user).order_by('-created_at')

    is_following = False
    if user.is_authenticated:
        is_following = user.following.filter(followed=profile_user).exists()
    return render(request, 'profile.html', {'profile': profile, 'posts': posts, 'profile_user': profile_user, 'user': user, 'is_following': is_following})


@login_required
def profile_edit(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return HttpResponseForbidden("У вас нет прав редактировать этот профиль.")

    profile = user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # ← добавили request.FILES
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if request.user == user_to_follow:
        messages.error(request, 'Вы не можете подписаться на самого себя!')
        return redirect('profile', username=username)

    if request.method=='POST':
        try:
            Follow.objects.create(follower=request.user, followed=user_to_follow)
            messages.success(request, f"Вы подписались на {username}")
        except IntegrityError:
            messages.warning(request, f"Вы уже подписаны на {username}")

    return redirect('profile', username=username)


@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)

    if request.method=='POST':
        Follow.objects.filter(
            follower=request.user,
            followed=user_to_unfollow
            ).delete()

        messages.success(request, f"Вы отписались от {username}")
    return redirect('profile', username=username)



@login_required
def followers(request, username):
    profile_user = get_object_or_404(User, username=username)
    followers = User.objects.filter(following__followed=profile_user)
    following = User.objects.filter(followers__follower=profile_user)
    return render(request, 'followers_list.html', {'followers':followers, 'following':following})

 
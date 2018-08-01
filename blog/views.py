from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string


# Create your views here.
def post_list(request):
    get_Post = Post.objects.all()
    search = request.GET.get('q')
    if search:
        get_Post = get_Post.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    paginator = Paginator(get_Post, 4)
    page = request.GET.get('page')
    total_article = paginator.get_page(page)

    context = {
        'post': total_article,
    }

    return render(request, 'blog/post_list.html', context)


def post_details(request, id, slug):
    post = get_object_or_404(Post, id=id)
    comments = comment.objects.filter(post=post,reply=None).order_by('-id')
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')  # content is the attr of model named comment
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = comment.objects.get(id=reply_id)
            comments = comment.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
            comments.save()
            return HttpResponseRedirect(post.get_absolute_url())

    else:
        comment_form = CommentForm()
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'comments': comments,
        'comment_form': comment_form,
    }
    if request.is_ajax():
        html = render_to_string('blog/comments.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'blog/post_details.html', context)


def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))  # came from value=post.id
    # post=get_object_or_404(Post,id=request.POST.get('id')) #came from value=post.id
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True

    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes()
    }

    if request.is_ajax():
        html = render_to_string('blog/like_section.html', context, request=request)
        return JsonResponse({'form': html})


def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
    else:
        form = PostCreateForm()
    context = {
        'form': form
    }

    return render(request, 'blog/post_create.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('blog:post_list'))
                else:
                    return HttpResponse('User is not Active')
            else:
                HttpResponse('User is none')

    form = UserLoginForm()

    context = {
        'form': form
    }

    return render(request, 'blog/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('blog:post_list')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            profile.objects.create(user=new_user)  # create empty user profile
            return redirect('blog:post_list')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST or None, instance=request.user.profile, files=request.Files)
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm()
        profile_form = ProfileEditForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'blog/edit_profile.html', context)

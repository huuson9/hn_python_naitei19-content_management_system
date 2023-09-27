from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Count
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm

# Create your views here.

from . models import Rating, User, Article, Like, Comment
from . forms import UserForm, CommentForm

#Customize user information
def showUserDetail(request, pk):
    user = get_object_or_404(User, id=pk)
    context = {'user': user}

    return render(request, 'home/user/user_detail.html' , context)

def updateUser(request, pk):
    user = get_object_or_404(User, id=pk)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user', pk=pk))
        
    else:
        form = UserForm(instance=user)
    
    context = {'form': form}

    return render(request, 'home/user/user_update.html' , context)

def articleList(request): 
    articles = Article.objects.all().order_by('-created_at')
    articles_feature = Article.objects.annotate(comment_count=Count('comment')).order_by('-comment_count')[:3]
    user = get_object_or_404(User, id=request.user.id)

    for article in articles:
        article.like = False

        if Like.objects.filter(user=user, article=article).exists():
            article.like = True

    for article in articles_feature:
        article.like = False
        
        if Like.objects.filter(user=user, article=article).exists():
            article.like = True
            
    context = {
        'article': articles, 
        'articles_feature': articles_feature,     
    }

    return render(request, 'index.html', context)

def articleDetail(request, pk): 
    article = get_object_or_404(Article, id=pk)
    comments = Comment.objects.filter(article=article).order_by('-created_at')
    rating = Rating.objects.filter(user=request.user.id, article=article).first()
    article.user_rating = rating.rating_value if rating else 0

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
    else: 
        comment_form = CommentForm()

    return render(request, 'home/article/article_detail.html', {'article': article,
                                                                'comments': comments,
                                                                'comment_form': comment_form})


#Like and rate article
def likeArticle(request, pk):
    article = get_object_or_404(Article, id=pk)
    user = get_object_or_404(User, id=request.user.id)
    check = 0
    
    if request.method == 'POST':
        like = Like.objects.filter(user=user, article=article)

        if not like.exists():
            Like.objects.create(user=user, article=article)
            check = 1
        else:
            like.delete()

    context = {
        'likes': article.count_likes(),
        'checked': check
    }

    return JsonResponse(context, safe=False)

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'registration/register.html', { 'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.bio = 'please enter your bio'
            user.profile_picture = '/static/images/user/default.jpg'
            user.username = user.username.lower()
            user.save()
            messages.success(request, _('You have singed up successfully.'))
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'registration/register.html', {'form': form})
                                                    

def rateArticle(request, post_id: int, rating: int):
    article = Article.objects.get(id=post_id)
    user = get_object_or_404(User, id=request.user.id)
    Rating.objects.filter(user=user, article=article).delete()
    Rating.objects.create(user=user, article=article, rating_value=rating)

    return articleDetail(request, post_id)

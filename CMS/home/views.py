from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count

# Create your views here.

from . models import Rating, User, Article, Like, Comment
from . forms import UserForm, CommentForm

#Home page
def home(request):
    articles = Article.objects.all().order_by("id")
    for article in articles:
        rating = Rating.objects.filter(user=request.user.id, article=article).first()
        article.user_rating = rating.rating_value if rating else 0

    context = {'articles': articles}

    return render(request, 'home.html', context)

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

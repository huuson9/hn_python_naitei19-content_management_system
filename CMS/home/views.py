from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.

from . models import User, Article
from . forms import UserForm

def index(request):
    return render(request, 'index.html')

def showUserDetail(request, pk):
    user = get_object_or_404(User, id=pk)
    context = {'user': user}

    return render(request, 'home/user/user_detail.html', context)

def updateUser(request, pk):
    user = get_object_or_404(User)
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user', pk=pk) 
        
    context = {'form': form}

    return render(request, 'home/user/user_update.html', context)

def articleList(request): 
    article = Article.objects.all().order_by('-created_at')
    context = {'article': article}
    return render(request, 'index.html', context)

def articleDetail(request, pk): 
    article = get_object_or_404(Article, id=pk)
    context = {'article': article}

    return render(request, 'home/article/article_detail.html', context)

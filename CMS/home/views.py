from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.

from . models import User
from . forms import UserForm

def showUserDetail(request, pk):
    user = get_object_or_404(User, id=pk)
    context = {'user': user}

    return render(request, 'home/user_detail.html', context)

def updateUser(request, pk):
    user = get_object_or_404(User, id=pk)
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user', pk=pk) 
        
    context = {'form': form}

    return render(request, 'home/user_update.html', context)

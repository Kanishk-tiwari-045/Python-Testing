from django.shortcuts import render, redirect
from .models import GitHubUser
from .forms import GitHubUserForm
from .utils import fetch_github_user

def get_user_info(request):
    if request.method == "POST":
        form = GitHubUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user_data = fetch_github_user(username)
            if user_data:
                github_user, created = GitHubUser.objects.update_or_create(
                    username=user_data['login'],
                    defaults={
                        'name': user_data.get('name', ''),
                        'company': user_data.get('company', ''),
                        'blog': user_data.get('blog', ''),
                        'location': user_data.get('location', ''),
                        'bio': user_data.get('bio', ''),
                        'public_repos': user_data.get('public_repos', 0),
                        'followers': user_data.get('followers', 0),
                        'following': user_data.get('following', 0),
                    }
                )
                return redirect('user_detail', username=username)
    else:
        form = GitHubUserForm()
    return render(request, 'github_user/get_user_info.html', {'form': form})

def user_detail(request, username):
    user = GitHubUser.objects.get(username=username)
    return render(request, 'github_user/user_detail.html', {'user': user})


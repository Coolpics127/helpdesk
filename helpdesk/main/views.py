from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from .forms import New_user_form, New_user_profile_form, New_request, User_edit_form, Request_response
from .models import Profile, Requests, Statuses, IP_map, LogPass, Customs

# Метод, который открывает начальную страницу
def index(request):
    return render(request, 'main/index.html')

# Метод, который открывает главную страницу
@login_required
def home(request):
    user = request.user
    is_admin = user.groups.filter(id='1').exists()
    is_moderator = user.groups.filter(id='2').exists()
    return render(request, 'main/home.html', {'is_admin': is_admin, 'is_moderator': is_moderator})


# ----------- ЗАЯВОЧНАЯ СИСТЕМА -----------
# Метод, который открывает страницу списка заявок
@login_required
def request_list(request):
    user = request.user
    is_admin = user.groups.filter(id='1').exists()
    is_moderator = user.groups.filter(id='2').exists()
    if user.groups.filter(id='1').exists() or user.groups.filter(id='2').exists():
        requests = Requests.objects.filter(is_deleted=False).order_by('-id')
        return render(request, 'main/requests.html',{'requests': requests, 'is_admin': is_admin, 'is_moderator': is_moderator})
    else:
        requests = Requests.objects.filter(is_deleted=False, issued_by=user).order_by('-id')
        return render(request, 'main/requests.html', {'requests': requests, 'is_admin': is_admin, 'is_moderator': is_moderator})

# Метод, который открывает страницу создания заявки
@login_required
def create_request(request):
    user = request.user
    is_admin = user.groups.filter(id='1').exists()
    is_moderator = user.groups.filter(id='2').exists()
    if request.method == 'POST':
        request_form = New_request(request.POST, request.FILES)
        if request_form.is_valid():
            req = request_form.save(commit=False)
            req.issued_by = request.user
            req.status = Statuses.objects.get(id='1')
            req.save()
            return redirect('requests')
    else:
        request_form = New_request()
    if user.groups.filter(id='1').exists():
        return render(request, 'main/new_request.html',{'request_form': request_form, 'is_admin': is_admin, 'is_moderator': is_moderator})
    else:
        return render(request, 'main/new_request.html', {'request_form': request_form, 'is_admin': is_admin, 'is_moderator': is_moderator})

def request_view(request, pk):
    user = request.user
    is_admin = user.groups.filter(id='1').exists()
    is_moderator = user.groups.filter(id='2').exists()
    request1 = Requests.objects.get(pk=pk)
    response_form = Request_response(instance=request1)
    instance_status = request1.status_id

    if request.method == 'POST':
        response_form = Request_response(request.POST, request.FILES, instance=request1)
        if response_form.is_valid():
                request1.save()
                return redirect('requests')
        else:
            response_form = Request_response()
        return render(request, 'main/request_view.html', {'is_admin': is_admin, 'is_moderator': is_moderator, 'request': request1, 'response_form': response_form, 'status': instance_status})
    else:
        return render(request, 'main/request_view.html', {'is_admin': is_admin, 'is_moderator': is_moderator, 'request': request1, 'response_form': response_form, 'status': instance_status})


# ----------- ИТ-АКТИВЫ -----------
# Метод, который открывает страницу закупок
@login_required
def supplies(request):
    user = request.user
    if user.groups.filter(id='1').exists():
        supplies = Customs.objects.all()
        return render(request, 'main/finances.html', {'supplies':supplies})
    else:
        return redirect('home')

# Метод, который открывает базу знаний
@login_required
def knoledge_base(request):
    user = request.user
    if user.groups.filter(id='1').exists():
        return render(request, 'main/knowledge_base.html')
    else:
        return redirect('home')

# Метод, который открывает страницу списка пользователей
@login_required
def user_list(request):
    user = request.user
    if user.groups.filter(id='1').exists():
        users = get_user_model().objects.all().order_by('last_name')
        return render(request, 'main/user_list.html', {'users':users})
    else:
        return redirect('home')

# Метод, который открывает страницу профиля пользователя
@login_required
def user_profile(request):
    user = request.user
    is_admin = user.groups.filter(id='1').exists()
    is_moderator = user.groups.filter(id='2').exists()
    return render(request, 'main/profile.html', {'is_admin': is_admin, 'is_moderator': is_moderator})

# Метод, который открывает страницу управления ИТ-активами
@login_required
def assets(request):
    user = request.user
    if user.groups.filter(id='1').exists():
        return render(request, 'main/assets.html')
    else:
        return redirect('home')

# Метод, который открывает страницу IP-адресов
@login_required
def ip_list(request):
    user = request.user
    if user.groups.filter(id='1').exists():
        ip_list = IP_map.objects.all()
        return render(request, 'main/ip_list.html', {'ip_list':ip_list})
    else:
        return redirect('home')

# Метод, который открывает страницу учетных записей
@login_required
def logpasslist(request):
    user = request.user
    if user.groups.filter(id='1').exists():
        logpass = LogPass.objects.all()
        return render(request, 'main/logpass_list.html', {'logpass':logpass})
    else:
        return redirect('home')

# Метод, который открывает страницу регистрации нового пользователя
@login_required
def register(request):
    user = request.user
    if user.groups.filter(id='1').exists():
        if request.method == 'POST':
            user_form = New_user_form(request.POST, request.FILES)
            profile_form = New_user_profile_form(request.POST, request.FILES)
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                profile = profile_form.save(commit = False)
                profile.user = user
                profile.save()
                return redirect('users')
        else:
            user_form = New_user_form()
            profile_form = New_user_profile_form()
        return render(request, 'main/new_user.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        return redirect('home')

# Метод, который открывает страницу просмотра профиля пользователя (из списка пользователей)
class UserProfileView(DetailView):
    model = User
    template_name = 'main/user_profile.html'
    context_object_name = 'user'

@login_required
def user_update(request, pk):

    user = User.objects.get(pk=pk)
    this_user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=pk)
    user_form = User_edit_form(instance=user)
    profile_form = New_user_profile_form(instance=profile)

    if request.method == 'POST':
        user_form = User_edit_form(request.POST, request.FILES, instance=user)
        profile_form = New_user_profile_form(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                return redirect('users')
        else:
            user_form = New_user_form()
            profile_form = New_user_profile_form()
        return render(request, 'main/user_edit.html', {'user_form': user_form, 'profile_form': profile_form, 'this_user': this_user})
    else:
        return render(request, 'main/user_edit.html', {'user_form': user_form, 'profile_form': profile_form, 'this_user': this_user})

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView
from .forms import New_user_form, New_user_profile_form, New_request
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

# Метод, который открывает страницу просмотра заявки (из списка заявок)
class RequestView(DetailView):
    model = Requests
    template_name = 'main/request_page.html'
    context_object_name = 'request'



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
            profile_form = New_user_profile_form(request.POST)
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

# Метод, который открывает страницу просмотра обновления пользователя (страницы просмотра профиля)
class UserProfileUpdate(UpdateView):
    model = Profile
    form_class = New_user_profile_form
    template_name = 'main/edit_user.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = New_user_form(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = New_user_form(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(UserProfileUpdate, self).form_valid(form)

    def get_absolute_url(self):
        return f'/users/{self.id}'
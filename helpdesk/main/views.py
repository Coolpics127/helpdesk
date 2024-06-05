from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from .forms import New_user_form, New_user_profile_form
from .models import Profile


def index(request):
    return render(request, 'main/index.html')

# Метод, который открывает (рендерит) страницу home.html
@login_required
def home(request):
    return render(request, 'main/home.html')

# Метод, который открывает (рендерит) страницу с заявками req_page.html
@login_required
def request_list(request):
    return render(request, 'main/req_page.html')

# Метод, который открывает страницу списка пользователей
@login_required
def user_list(request):
    users = get_user_model().objects.all()
    return render(request, 'main/user_list.html', {'users':users})

# Метод, который открывает страницу профиля пользователя
@login_required
def user_profile(request):
    return render(request,'main/profile.html')

@login_required
def register(request):
    if request.method == 'POST':
        user_form = New_user_form(request.POST)
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

class UserProfileView(DetailView):
    model = User
    template_name = 'main/user_profile.html'
    context_object_name = 'user'

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
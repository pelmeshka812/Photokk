from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, LoginView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from accounts import forms
from accounts.forms import LoginForm, UserRegistrationForm, ProfileForm
from accounts.models import Profile, Subscribe
from django.contrib import messages

from blog.decorators import ajax_required

"""
class SignUp(generic.CreateView):
    
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/registration.html'


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Authenern')  # поменяй потом !!!!
            else:
                return HttpResponse('Disable idi nax')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})"""


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form = LoginForm
    redirect_authenticated_user = 'blog/'


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            new_user.save()
            return render(request,
                          'accounts/register_done.html',
                          {'new_user': new_user, }, )
        return render(request,
                      'accounts/registration.html',
                      {'user_form': user_form, }, )
    else:
        user_form = UserRegistrationForm()
        return render(request,
                      'accounts/registration.html',
                      {'user_form': user_form, }, )


@login_required
def user_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileForm(instance=request.user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен')
        else:
            messages.error(request, 'Что-то пошло не так')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request,
                  'accounts/profile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class ProfileListView(ListView):
    template_name = 'accounts/user/user_list.html'
    model = Profile
    context_object_name = 'profiles'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Profile.objects.exclude(user=self.request.user)
        else:
            return Profile.objects.all()


class ProfileDetailView(DetailView):
    model = Profile
    pk_url_kwarg = 'id'
    context_object_name = 'profile'


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    subject_template_name = 'email/reset_letter_subject.txt'
    email_template_name = 'email/reset_letter_body.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    form_class = PasswordResetForm
    from_email = EMAIL_HOST_USER


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_complete.html'


@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'accounts/user/user_list.html', {'section': 'people',
                                                            'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'accounts/user/user_detail.html',
                  {'section': 'people',
                   'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    print(action)
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            print(user.username)
            if action == 'follow':
                Subscribe.objects.get_or_create(user_from=request.user, user_to=user)
            else:
                Subscribe.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})

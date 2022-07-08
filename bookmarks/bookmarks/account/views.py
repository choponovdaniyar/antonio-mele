from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import LoginForm, ProfileEditForm, UserEditForm, UserRegistrationForm
from .models import Profile, Contact

from common.decorators import ajax_required, is_ajax
from actions.utils import create_action
from actions.models import Action


@login_required
def dashboard(request):
    # По умолчанию отображаем все действия.
    actions = Action.objects.all()#.exclude(user=request.user)
    # following_ids = request.user.followings.values_list('id', flat=True)
    # if following_ids:
    #     # Если текущий пользователь подписался на кого-то,
    #     # отображаем только действия этих пользователей
    #     actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user').prefetch_related('target')
    paginator = Paginator(actions, 5)
    page = request.GET.get('page')
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        # Если переданная страница не является числом, возвращаем первую
        actions = paginator.page(1)
    except EmptyPage:
        # Если получили AJAX-запрос с номером страницы, большим, чем их количество, возвращаем пустую страниц
        if is_ajax(request):
            return HttpResponse('') 
        # Если номер страницы больше, чем их количество, возвращаем последнюю
        actions = paginator.page(paginator.num_pages)
    if is_ajax(request):
        return render(request, 'actions/action/list_ajax.html',{
            'actions': actions
        })
    return render(
        request, 
        'account/dashboard.html', 
        {
            'section': 'dashboard',
            'actions': actions
        }
    )    



class EditProfileView(View):
    template_name = 'account/edit.html'

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, 
            data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile update successfully')
        else:
            messages.error(request, 'Error updating your profile')
        
        return render(request, template_name=self.template_name, 
            context={'user_form': user_form, 'profile_form': profile_form})


    def get(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user)
        try:
            request.user.profile
        except:
            Profile.objects.create(user=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
        return render(request, template_name=self.template_name, 
            context={'user_form': user_form, 'profile_form': profile_form})



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем пользователя в базе данных.
            new_user.save()
            create_action(new_user, 'has created an account')
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html',
                {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(
        request,
        'account/user/list.html',
        {
            'section': 'people', 
            'users': users
        }
    )


@login_required
def user_detail(request, username): 
    user = get_object_or_404(User, username=username, is_active=True)
    print(user.followers)
    return render(request,
        'account/user/detail.html',
        {
            'section': 'people',
            'user': user
        }
    )


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    print(user_id, action)
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({"status": "ok"})
        except User.DoesNotExist:
            return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "ok"})

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout


from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def login(request):
    template_data = {'title': 'Login'}

    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST.get('role', 'user')

        user = authenticate(request, username=username, password=password)

        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)

        if role == 'admin':
            if user.is_staff:
                return redirect('/admin/')
            else:
                template_data['error'] = 'You are not an admin.'
                return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            return redirect('trivias.index')


def signup(request):
    template_data = {'title': 'Sign Up'}

    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})

    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        role = request.POST.get('role', 'user')

        if form.is_valid():
            user = form.save(commit=False)

            if role == 'admin':
                user.is_staff = True
            else:
                user.is_staff = False

            user.save()
            return redirect('accounts.login')

        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})


@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts.login')

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
                  {'template_data': template_data})
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from product.models import Category

from user.models import UserProfile
from user.forms import SignUpForm
# Create your views here.
from user.forms import UserUpdateForm, ProfileUpdateForm

from order.models import Order,OrderProduct

from product.models import Comment


def index(request):
    return HttpResponse('User')


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            # Redirect to a success page.
            HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Fail !! Username or password is incorrect")
            return HttpResponseRedirect('/user/login')
    # create data in profile table for user

    categories = Category.objects.all()
    context = dict(categories=categories)
    return render(request, 'login_form.html', context)


def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            #create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id=current_user.id
            data.image='user/user.png'
            data.save()
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/user/signup')

    form = SignUpForm()
    categories = Category.objects.all()
    context = dict(categories=categories, form=form)
    return render(request, 'signup_form.html', context)


def logout_form(request):
    logout(request)
    return HttpResponseRedirect('/')


def checkout_form(request):
    categories = Category.objects.all()
    context = dict(categories=categories)
    return render(request, 'checkout_form.html', context)


def userprofile_form(request):
    categories = Category.objects.all()

    profile = UserProfile.objects.get(user_id=request.user.id)
    context = dict(categories=categories, profile=profile)

    return render(request, 'userprofile_form.html', context)


@login_required(login_url='/user/login') # Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user/userprofile')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) #"userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/user/login') # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user/userprofile')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        #category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form,#'category': category
                       })


@login_required(login_url='/user/login') # Check login
def user_orders(request):
    #category = Category.objects.all()
    current_user = request.user
    orders=Order.objects.filter(user_id=current_user.id)
    context = {#'category': category,
               'orders': orders,
               }
    return render(request, 'user_orders.html', context)


@login_required(login_url='/user/login') # Check login
def user_orderdetail(request,id):
    categories = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'categories': categories,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/user/login') # Check login
def user_order_product(request):
    categories = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
    context = {'categories': categories,
               'order_product': order_product,
               }
    return render(request, 'user_order_products.html', context)


@login_required(login_url='/user/login') # Check login
def user_order_product_detail(request,id,oid):
    categories = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id,user_id=current_user.id)
    context = {
        'categories': categories,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)


def user_comments(request):
    categories = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'categories': categories,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/user/login') # Check login
def user_deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/comments')
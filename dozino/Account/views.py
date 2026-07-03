from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import re
User = get_user_model()

##C>messages 

def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        
        phone_number = request.POST.get('phone_number')
        if not re.match(r'^09\d{9}$', phone_number):
          messages.error(request,'شماره موبایل معتبر نیست')
          return redirect('register')
        
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'رمزهای وارد شده مطابقت ندارند')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'این نام کاربری از قبل وجود دارد')
            return redirect('register')

        if User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'این شماره تلفن از قبل وجود دارد')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            password=password,
            phone_number=phone_number
        )

        auth.login(request, user)

        messages.success(request,'ثبت نام با موفقیت انجام شد' )
        return redirect('index')

    return render(request, 'Account/register.html')


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
          login(request, user)
             ##C>>if user is tailor
          messages.success(request,'شما با موفقیت وارد سایت شدید' )
          return redirect('index')
        print("USERNAME:", repr(username))
        print("PASSWORD:", repr(password))
        messages.error( request,'نام کاربری یا رمز عبور اشتباه است' )
        return redirect('login')

    return render(request, 'Account/login.html')


@login_required #just users  that logged in already 
def user_logout(request):

    if request.method == 'POST':

        auth.logout(request)

        messages.success(request,'شما از حساب کاربری خود خارج شدید')

    return redirect('index')


@login_required
def profile(request):

    if request.method == 'POST':


        print(request.POST)
        user = request.user
        user.username=request.POST.get('username')
        user.full_name=request.POST.get('full_name')

        new_phone = request.POST.get('phone_number')
        if not re.match(r'^09\d{9}$', new_phone):
          messages.error(request,'شماره موبایل معتبر نیست')
          return redirect('profile')
        ###C>check below part
        if User.objects.filter(phone_number=new_phone).exclude(id=user.id).exists():
          messages.error(request,'این شماره قبلاً استفاده شده')
          return redirect('profile')        
        user.phone_number = new_phone

        user.gender=request.POST.get('gender')
        user.address = request.POST.get('address')
        
        postal_code=request.POST.get('postal_code')
        if not re.match(r'^\d{10}$', postal_code):
          messages.error(request, 'کد پستی باید 10 رقم باشد')
          return redirect('profile')
        user.postal_code=postal_code
        ##profle image
        user.save()

        messages.success( request,'اطلاعات پروفایل با موفقیت بروزرسانی شد')
        return redirect('profile')

    return render(request,'Account/profile.html',{ 'user': request.user})


def resetpassword(request):
    if request.method == 'POST':

        step= request.POST.get('step')

        if step=='verify':
            code=request.POST.get('codeInput')
            if code=='123456' :
                return redirect('new_pass')
            
            messages.error(request,'کد وارد شده صحیح نیست')
            return render(request , 'Account/reset.html', {'show_form2':True})

        else:

            phone_number = request.POST.get('phone_number')
            if not re.match(r'^09\d{9}$', phone_number):
              messages.error(request,'شماره موبایل معتبر نیست')
              return redirect('resetpassword')

        user = User.objects.filter(phone_number=phone_number).first()

        if user:

            request.session['reset_user_id'] = user.id
            return render(request , 'Account/reset.html', {'show_form2':True})


        messages.error(request,'کاربری با این شماره یافت نشد')
        return redirect('resetpassword')

    return render(request, 'Account/reset.html')


def new_password(request):

    if request.method == 'POST':

        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:

            messages.error(request,'رمزها مطابقت ندارند')
            return redirect('new_pass')

        user_id = request.session.get('reset_user_id')

        if not user_id:

            return redirect('resetpassword')

        user = User.objects.get(id=user_id)

        user.set_password(password)
        user.save()

        del request.session['reset_user_id']

        messages.success(request,'رمز عبور با موفقیت تغییر کرد')
        return redirect('login')

    return render(request,'Account/new_pass.html')
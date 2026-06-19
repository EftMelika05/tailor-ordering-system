from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()


def register(request):

    if request.method == 'POST':

        role = request.POST.get('role')
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_Number')
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
            role=role,
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

        user = auth.authenticate(username=username, password=password )

        if user is not None:
              
              auth.login(request, user)

              if user.role == 'customer':
                 messages.success(request,'شما وارد سایت شدید' )
                 return redirect('index')

              elif user.role == 'tailor':
                  messages.success(request,'شما وارد سایت شدید' )
                  return redirect('tailor_panel')
              

        messages.error( request,'نام کاربری یا رمز عبور اشتباه است' )
        return redirect('login')

    return render(request, 'Account/login.html')


@login_required
def user_logout(request):

    if request.method == 'POST':

        auth.logout(request)

        messages.success(request,'شما از حساب کاربری خود خارج شدید')

    return redirect('index')


@login_required
def profile(request):

    if request.method == 'POST':

        user = request.user

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        new_phone = request.POST.get('phone_number')
        if User.objects.filter(phone_number=new_phone).exclude(id=user.id).exists():
          messages.error(request,'این شماره قبلاً استفاده شده')
          return redirect('profile')
        
        user.phone_number = new_phone

        user.postal_code = request.POST.get('postal_code')
        user.address = request.POST.get('address')
        
        user.save()

        messages.success( request,'اطلاعات پروفایل با موفقیت بروزرسانی شد')

        return redirect('profile')

    return render(request,'Account/profile.html',
                  { 'user': request.user})


def resetpass(request):

    if request.method == 'POST':

        phone_number = request.POST.get('phone_number')

        user = User.objects.filter(phone_number=phone_number).first()

        if user:

            request.session['reset_user_id'] = user.id

            return redirect('resetpassword')

        messages.error(request,'کاربری با این شماره یافت نشد')

        return redirect('resetpassword')

    return render(
        request,
        'Account/reset.html'
    )


def new_password(request):

    if request.method == 'POST':

        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:

            messages.error(request,'رمزها مطابقت ندارند')

            return redirect('new_password')

        user_id = request.session.get('reset_user_id')

        if not user_id:

            return redirect('resetpass')

        user = User.objects.get(id=user_id)

        user.set_password(password)
        user.save()

        del request.session['reset_user_id']

        messages.success(request,'رمز عبور با موفقیت تغییر کرد')

        return redirect('login')

    return render(
        request,
        'Account/new_password.html'
    )
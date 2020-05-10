from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mainapp.models import Post
from django.urls import reverse
import math
from accounts.forms import (
    RegisterForm,
    LoginForm,
    ProfileUpdateUserForm,
    ProfileUpateMetaForm,
)
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.core.paginator import Paginator

#register view 
def RegisterView(request):
    if request.method =='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account created Successfully! now you can login')
            return redirect('users:login')
    else:
        form=RegisterForm()
    return render(request,'accounts/register.html',{'form':form,'title':'Register'})

class MyLoginView(LoginView):
    template_name='accounts/login.html'
    context_object_name='form'
    class Meta:
        form_class=LoginForm
class MyLogoutView(LogoutView):
    template_name='accounts/logout.html'


def ProfileView(request,uname):
    try:
        requested_user=User.objects.get(username=str(uname))
        posts=Post.objects.filter(author_id=requested_user.id).order_by('-date_posted')
        total=len(posts)
        for post in posts:
            post.title=post.title[0:38]+' -'
            post.content=post.content[0:49]+' ....'
        paginator=Paginator(posts,6)
        temp=request.GET.get('page')
        print('fine1')
        page_number=1
        if temp !=None:
            page_number=temp
        print('fine3')  
        page_obj=paginator.get_page(page_number)
        print('fine4')
        p_r=paginator.page_range
        page_list=[]
        for i in p_r:
            if abs(page_obj.number-i) <=3:
                page_list.append(i)
        print('fine5')
        last=math.ceil(paginator.count/6)
        print('fine2')
        return render(request,'accounts/profile.html',{'title':'Profile','requested_user':requested_user,'page_obj':page_obj,'page_list':page_list,'last':last,'total':total})
    except:
        return render(request,'accounts/pagenotfound.html',{'title':'page not found!'})

@login_required
def EditProfielView(request,uname):
    try:
        request_user=User.objects.filter(username=str(uname)).first()
        user=request.user
        if request_user!=user:
            return render(request,'accounts/pagenotfound.html',{'title':'page not found!'})
        if request.method=='POST':
            form1=ProfileUpdateUserForm(request.POST,request.FILES,instance=user)
            form2=ProfileUpateMetaForm(request.POST,request.FILES,instance=user.profile)
            if form1.is_valid() and form2.is_valid():
                form1.save()
                form2.save()
                return redirect(reverse('users:profile',kwargs={'uname':user.username}))
        else:
            form1=ProfileUpdateUserForm(instance=user)
            form2=ProfileUpateMetaForm(instance=user.profile)
        return render(request,'accounts/editprofile.html',{'form1':form1,'form2':form2})
    except:
        return render(request,'accounts/pagenotfound.html',{'title':'page not found!'})

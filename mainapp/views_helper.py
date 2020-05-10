from django.contrib.auth.models import User
from django.shortcuts import render,reverse,redirect
from mainapp.models import Post,Comment
from accounts.models import Profile
from mainapp.forms import CommentForm
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import math
@login_required
def CommentDisplayView(request,id,c_id):
    if request.method=='POST':
        try:
            post=Post.objects.get(id=id)
            comment=Comment.objects.get(id=c_id)
            form=CommentForm(instance=comment)
            return render(request,'mainapp/commentedit.html',{'form':form})
        except:
            return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
    else:
        return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
@login_required
def CommentEditView(request,id,c_id):
    if request.method=='POST':
        try:
            post=Post.objects.get(id=id)
            comment=Comment.objects.get(id=c_id)
            form=CommentForm(request.POST)
            if form.is_valid():
                content=form.cleaned_data.get('content')
                comment.content=content
                comment.save()
                return redirect(reverse('post:post-detail',kwargs={'id':id}))
            return render(request,'mainapp/commentedit.html',{'form':form})
        except:
            return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
    else:
        return redirect(reverse('post:post-comment-view',kwargs={'id':id,'c_id':c_id}))
@login_required
def CommentDeleteView(request,id,c_id):
    if request.method=='POST':
        try:
            post=Post.objects.get(id=id)
            comment=Comment.objects.get(id=c_id)
            comment.delete()
            return redirect(post.get_absolute_url())
        except:
            return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
    else:
        return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
@login_required
def CommentUpvoteView(request,id,c_id):
    if request.method=='POST':
        try:
            comment=Comment.objects.get(id=c_id)
            user=request.user
            if comment.comment_downvoted_users.filter(id=user.id).exists():
                comment.comment_downvoted_users.remove(user)
                comment.comment_upvoted_users.add(user)
            elif comment.comment_upvoted_users.filter(id=user.id).exists():
                comment.comment_upvoted_users.remove(user)
            else:
                comment.comment_upvoted_users.add(user)
            comment.set_comment_upvote_count()
            comment.set_comment_downvote_count()
            comment.save()
            return redirect(reverse('post:post-detail',kwargs={'id':id,}))
        except:
            return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
    else:
        return redirect(reverse('post:post-detail',kwargs={'id':id}))

@login_required
def CommentDownvoteView(request,id,c_id):
    if request.method=='POST':
        try:
            comment=Comment.objects.get(id=c_id)
            user=request.user
            if comment.comment_upvoted_users.filter(id=user.id).exists():
                comment.comment_upvoted_users.remove(user)
                comment.comment_downvoted_users.add(user)
            elif comment.comment_downvoted_users.filter(id=user.id).exists():
                comment.comment_downvoted_users.remove(user)
            else:
                comment.comment_downvoted_users.add(user)
            comment.set_comment_upvote_count()
            comment.set_comment_downvote_count()
            comment.save()
            return redirect(reverse('post:post-detail',kwargs={'id':id,}))
        except:
            return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
    else:
        return redirect(reverse('post:post-detail',kwargs={'id':id,}))

def SearchView(request):
    search_query=request.GET.get('q')
    user_query_set=Profile.objects.filter(user__username__icontains=search_query)
    post_query_set=Post.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query)).distinct().order_by('-date_posted')
    user_count=user_query_set.count()
    post_count=post_query_set.count()
    user_paginator=Paginator(user_query_set,3)
    temp_user=request.GET.get('user-search')
    user_page_number=1
    if temp_user!=None:
        user_page_number=temp_user
    user_page_obj=user_paginator.get_page(user_page_number)
    print(user_page_obj)
    user_total=user_query_set.count()
    paginator=Paginator(post_query_set,7)
    temp=request.GET.get('page')
    page_number=1
    if temp !=None:
        page_number=temp  
    page_obj=paginator.get_page(page_number)
    page_range=paginator.page_range
    total=len(post_query_set)
    page_list=[]
    for i in page_range:
        if abs(page_obj.number-i) <=3:
            page_list.append(i)
    last=math.ceil(paginator.count/7)
    context={
        'user_page_obj':user_page_obj,
        'page_obj':page_obj,
        'page_list':page_list,
        'last':last,
        'total':total,
        'user_total':user_total,
        'user_page_obj':user_page_obj,
        'user_count':user_count,
        'post_count':post_count,
    }
    return render(request,'mainapp/search.html',context)
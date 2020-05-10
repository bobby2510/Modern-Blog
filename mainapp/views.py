from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from mainapp.forms import CreatePostForm,CommentForm
from mainapp.models import Post,Comment,PostTag
from django.contrib.auth.models import User,AnonymousUser
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Count,Sum
import json
import math  

def home_helper(queryset,tag_filter_list):
    if tag_filter_list is None:
        return queryset
    else:
        return queryset.filter(tags__name__in=tag_filter_list).distinct()
def Home(request):
    f_type=request.GET.get('filter')
    json_encoded_string=request.GET.get('tag')
    tag_filter_list=None
    if not json_encoded_string is None:
        json_obj=eval(json_encoded_string)
        tag_filter_list=json_obj['tags']
    if f_type==None:
        f_type=0
    f_type=int(f_type)
    queryset=Post.objects.all()
    queryset=home_helper(queryset,tag_filter_list)
    if f_type ==2:
        posts=queryset.order_by('-points','-author_id')
    else:
        posts=queryset.order_by('-date_posted')
    for post in posts:
        post.title=post.title[0:38]+' -'
        post.content=post.content[0:49]+' ....'
    paginator=Paginator(posts,6)
    temp=request.GET.get('page')
    page_number=1
    if temp !=None:
        page_number=temp  
    page_obj=paginator.get_page(page_number)
    page_range=paginator.page_range
    total=len(posts)
    page_list=[]
    for i in page_range:
        if abs(page_obj.number-i) <=3:
            page_list.append(i)
    last=math.ceil(paginator.count/6)
    tag_query_set=PostTag.objects.values('name').annotate(post_count=Count('posts'))
    user_likes=0
    user_posts=0
    if request.user.is_authenticated:
        user=request.user
        user_likes=Post.objects.filter(author__username=user.username).aggregate(like_count=Sum('upvote_count')).get('like_count')
        user_posts=Post.objects.filter(author__username=user.username).count()
    return render(request,'mainapp/home.html',{'page_obj':page_obj,'tag_filter_list':tag_filter_list,
    'page_list':page_list,'last':last,'total':total,'tag_query_set':tag_query_set,
    'f_type':f_type,'user_likes':user_likes,'user_posts':user_posts})

def About(request):
    return render(request,'mainapp/about.html',{'title':'About Us'})
@login_required
def CreatePost(request):
    tag_list=PostTag.objects.all()
    if request.method=='POST':
        form=CreatePostForm(request.POST,request.FILES)
        if form.is_valid():
            form.instance.author=request.user
            tag_query_set=PostTag.objects.filter(name__in=request.POST.getlist('tags'))
            form.instance.save()
            if tag_query_set.count()==0:
                form.instance.tags.add(PostTag.objects.get('General'))
            else:
                for tag in tag_query_set:
                    form.instance.tags.add(tag)
            return redirect(form.instance.get_absolute_url())
    else:
        form=CreatePostForm()
    return render(request,'mainapp/createpost.html',{'form':form,'title':'Create Post','tag_list':tag_list})
    
def PostDetail(request,id):
    try:
        page=1
        f_type=1
        if request.GET.get('page') !=None:
            page=request.GET.get('page')
        if request.GET.get('filter')!=None:
            f_type=request.GET.get('filter')
        post=Post.objects.get(pk=id)
        f_type=int(f_type)
        if f_type==2:
            comment_list=Comment.objects.filter(post=post).order_by('-comment_upvote_count','-date_commented')
        else:
            comment_list=Comment.objects.filter(post=post).order_by('-date_commented')
        paginator=Paginator(comment_list,5)
        page_obj=paginator.get_page(page)
        page_range=paginator.page_range
        total=len(comment_list)
        page_list=[]
        for i in page_range:
            if abs(page_obj.number-i) <=3:
                page_list.append(i)
        last=math.ceil(paginator.count/5)
        upvoted_set={-1,}
        downvoted_set={-1,}
        if request.user.is_authenticated:
            upvote=False
            downvote=False
            user=request.user 
            if post.upvoted_users.filter(id=user.id).exists():
                upvote=True
            elif post.downvoted_users.filter(id=user.id).exists():
                downvote=True
            form=CommentForm()
            for comment in comment_list:
                if comment.comment_upvoted_users.filter(id=user.id).exists():
                    upvoted_set.add(comment.id)
                if comment.comment_downvoted_users.filter(id=user.id).exists():
                    downvoted_set.add(comment.id)
            return render(request,'mainapp/postdetail.html',
            {'post':post,
            'upvote':upvote,
            'downvote':downvote,
            'comment_write':True,
            'form':form,
            'page_obj':page_obj,
            'page_list':page_list,
            'last':last,
            'total':total,
            'upvoted_set':upvoted_set,
            'downvoted_set':downvoted_set,})
        else:
            return render(request,'mainapp/postdetail.html',
            {'post':post,
            'comment_write':False,
            'page_obj':page_obj,
            'page_list':page_list,
            'upvoted_set':upvoted_set,
            'downvoted_set':downvoted_set,})
    except:
        return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
@login_required
def DelatePost(request,id):
    if request.method=='POST':
        user=request.user
        try:
            post=Post.objects.get(id=id)
            if post.author==user:
                post.delete()
                return redirect('home')
            else:
                return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
        except:
            return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
    else:
        return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})

@login_required
def EditPostView(request,id):
    if request.method=='POST':
        try:
            post=Post.objects.get(id=id)
            user=request.user
            if user==post.author:
                form=CreatePostForm(instance=post)
                return render(request,'mainapp/editpost.html',{'form':form})
            else:
                return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
        except:
            return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
    else:
        return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
 
@login_required
def EditPostSave(request,id):
    if request.method=='POST':
        try:
            post=Post.objects.get(id=id)
            user=request.user
            if user==post.author:
                form=CreatePostForm(request.POST,request.FILES,instance=post)
                if form.is_valid():
                    form.save()
                    return redirect(reverse('post:post-detail',kwargs={'id':post.id}))
                else:
                    return render(request,'mainapp/editpost.html',{'form':form})
            else:
                return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
        except:
            return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
    else:
        return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
@login_required
def UpvoteView(request,id):
    if request.method=='POST':
        try:
            post=Post.objects.get(id=id)
            user=request.user
            if post.downvoted_users.filter(id=user.id).exists():
                post.downvoted_users.remove(user)
                post.upvoted_users.add(user)
            elif post.upvoted_users.filter(id=user.id).exists():
                post.upvoted_users.remove(user)
            else:
                post.upvoted_users.add(user)
            post.set_upvote_count()
            post.set_downvote_count()
            post.set_points()
            post.save()
            return redirect(reverse('post:post-detail',kwargs={'id':post.id,}))
        except:
            return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
    else:
        return redirect(reverse('post:post-detail',kwargs={'id':id}))
@login_required
def DownvoteView(request,id):
    if request.method=='POST':
        try:
            post=Post.objects.get(id=id)
            user=request.user
            if post.upvoted_users.filter(id=user.id).exists():
                post.upvoted_users.remove(user)
                post.downvoted_users.add(user)
            elif post.downvoted_users.filter(id=user.id).exists():
                post.downvoted_users.remove(user)
            else:
                post.downvoted_users.add(user)
            post.set_upvote_count()
            post.set_downvote_count()
            post.set_points()
            post.save()
            return redirect(reverse('post:post-detail',kwargs={'id':post.id,}))
        except:
            return render(request,'accounts/pagenotfound.html',{'title':'HTTP 404 ERROR'})
    else:
        return redirect(reverse('post:post-detail',kwargs={'id':id}))

@login_required
def CommentView(request,id):
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            content=form.cleaned_data.get('content') 
            post=Post.objects.filter(id=id).first()
            user=request.user
            Comment.objects.create(post=post,user=user,content=content)
            post.set_comment_count()
            post.save()
    return redirect(reverse('post:post-detail',kwargs={'id':id}))
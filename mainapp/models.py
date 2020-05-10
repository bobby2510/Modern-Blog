
from django.db import models
from django.utils import timezone  
from django.contrib.auth.models import User
from django.urls import reverse

class PostTag(models.Model):
    name=models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=50)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    post_thumnail=models.ImageField(blank=True,null=True,upload_to='post_thumbnails')
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='author')
    upvoted_users=models.ManyToManyField(User,blank=True,related_name='upvote')
    downvoted_users=models.ManyToManyField(User,blank=True,related_name='downvote')
    upvote_count=models.IntegerField(default=0)
    downvote_count=models.IntegerField(default=0)
    comments=models.ManyToManyField(User,through='Comment',through_fields=('post','user'),blank=True,related_name='comments')
    comment_count=models.IntegerField(default=0)
    points=models.IntegerField(default=0)
    tags=models.ManyToManyField(PostTag,blank=True,related_name='posts')
    def __str__(self):
        return f'post - {self.title}'
    def get_absolute_url(self,*args,**kwargs):
        return reverse('post:post-detail',kwargs={'id':self.id})
    def time_ago(self):
        tp=self.date_posted
        tn=timezone.now()
        return self.time_calc(tp,tn)
    #finding time since posted
    def time_calc(self,tp,tn):
        if tn.year-tp.year >0:
            return str(tn.year-tp.year) + ' years ago'
        if tn.month-tp.month >0:
            return str(tn.month-tp.month) +' months ago'
        if tn.day-tp.day >0:
            return str(tn.day-tp.day) + ' days ago'
        if tn.hour-tp.hour >0:
            return str(tn.hour-tp.hour) +' hours ago'
        if tn.minute-tp.minute >0:
            return str(tn.minute-tp.minute) + ' minutes ago'
        if tn.second-tp.second >0:
            return str(tn.second-tp.second) + ' seconds ago'
        else:
            return 'just now'
    def set_upvote_count(self):
        self.upvote_count=self.upvoted_users.count()
    def set_downvote_count(self):
        self.downvote_count=self.downvoted_users.count()
    def set_comment_count(self):
        self.comment_count=Comment.objects.filter(post=self).count()
    def set_points(self):
        self.points=self.upvote_count-self.downvote_count

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comment_post')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment_user')
    content=models.TextField()
    comment_upvoted_users=models.ManyToManyField(User,related_name='comment_upvoted_users')
    comment_downvoted_users=models.ManyToManyField(User,related_name='comment_downvoted_users')
    comment_upvote_count=models.IntegerField(default=0)
    comment_downvote_count=models.IntegerField(default=0)
    date_commented=models.DateTimeField(default=timezone.now)

    def set_comment_upvote_count(self):
        self.comment_upvote_count=self.comment_upvoted_users.count()
    def set_comment_downvote_count(self):
        self.comment_downvote_count=self.comment_downvoted_users.count()

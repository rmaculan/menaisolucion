from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext as _
from notification.models import Notification
from django.dispatch import receiver
import uuid

def user_directory_path(instance, filename):
    if hasattr(instance, 'author'):
        return f'post_{instance.author.id}/{filename}'
    elif hasattr(instance, 'user'): 
        return f'user_{instance.user.id}/{filename}'
    else:
        raise ValueError("Instance requires 'author' or 'user'.")

# blog post model
class Post(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        )
    job_title = models.CharField(max_length=200, blank=True)
    picture = models.ImageField(
        upload_to=user_directory_path, 
        verbose_name="Picture", 
        default=""
        )
    video = models.URLField(blank=True, null=True, verbose_name="Video", default="")
    caption = models.CharField(
        max_length=10000, 
        verbose_name="Caption", 
        default=""
        )
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='draft'
        )
    on_delete=models.CASCADE
    likes = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0) 

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            queryset = Post.objects.all()
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            count = queryset.filter(slug__startswith=base_slug).count()

            if count > 0:
                # Initialize temp_slug before the loop
                temp_slug = f"{base_slug}-1"  # Start with an initial value
                i = 1
                while True:
                    if queryset.filter(slug=temp_slug).exists():
                        i += 1
                        temp_slug = f"{base_slug}-{i}"
                    else:
                            self.slug = temp_slug
                            break
            else:
                self.slug = base_slug
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post-details", args=[str(self.id)])
    
class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        related_name='comments', 
        on_delete=models.CASCADE
        )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
        )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        related_name='replies', 
        on_delete=models.CASCADE
        )
    
    class Meta:
        ordering = ['-created_at']

    def create_notification(self):
        """
        Creates a notification related to this comment instance.
        """
        post = self.post
        sender = self.author
        text_preview = self.content[:90]  
        notify = Notification.objects.create(
            post=post,
            sender=sender,
            user=post.author,
            text_preview=text_preview,
            notification_types=2
        )
        notify.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
        self.create_notification()

    @staticmethod
    def user_comment_post(sender, instance, created, **kwargs):
        if created:
            instance.create_notification()

    def user_del_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        sender = comment.author
        notify = Notification.objects.filter(
            post=post, 
            sender=sender, 
            user=post.author, 
            notification_types=2
            )
        notify.delete()
    
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name="post_likes"
        )

    def user_liked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification(post=post, sender=sender, user=post.user)
        notify.save()

    def user_unliked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification.objects.filter(
            post=post, 
            sender=sender, 
            notification_types=1
            )
        notify.delete()

class Follow(models.Model):
    follower = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='follower'
        )
    following = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='following'
        )

    def user_follow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following
        notify = Notification(
            sender=sender, 
            user=following, 
            notification_types=3
            )
        notify.save()

    def user_unfollow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following
        notify = Notification.objects.filter(
            sender=sender, 
            user=following, 
            notification_types=3
            )
        notify.delete()

@receiver(post_save, sender=Comment)
def comment_saved(sender, instance, created, **kwargs):
    if created:
        instance.user_comment_post(
            sender, 
            instance, 
            created, 
            **kwargs
            )

post_save.connect(
    Likes.user_liked_post, 
    sender=Likes
    )
post_delete.connect(
    Likes.user_unliked_post, 
    sender=Likes
    )

post_save.connect(
    Follow.user_follow, 
    sender=Follow
    )

post_delete.connect(
    Follow.user_unfollow, 
    sender=Follow
    )

post_save.connect(
    Comment.user_comment_post, 
    sender=Comment
    )
post_delete.connect(
    Comment.user_del_comment_post, 
    sender=Comment
    )    
   


from django.db import models
from user.models import User

class Image(models.Model):
    class Meta:
        db_table = 'image'

    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    before_image = models.ImageField(upload_to="befor_image", blank=True, null=True)
    after_image = models.ImageField(upload_to="after_image", blank=True, null=True)

class Post(models.Model):
    class Meta:
        db_table = 'post'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='images')
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    def __str__(self):
        return str(self.content)
        
class Comment(models.Model):
    class Meta:
        db_table = 'comment'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)
        
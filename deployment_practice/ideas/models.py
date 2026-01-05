from django.db import models

# Create your models here.
class DevTool(models.Model):
    """개발툴 모델"""
    KIND_CHOICES = [
        ('frontend', 'Frontend Framework'),
        ('backend', 'Backend Framework'),
        ('database', 'Database'),
        ('language', 'Programming Language'),
        ('devops', 'DevOps'),
        ('design', 'Design Tool'),
        ('etc', 'Etc'),
    ]
    
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Idea(models.Model):
    """아이디어 모델"""
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ideas/')
    content = models.TextField()
    interest = models.IntegerField(default=0)
    star_count = models.IntegerField(default=0)
    devtool = models.ForeignKey(DevTool, on_delete=models.CASCADE, related_name='ideas')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
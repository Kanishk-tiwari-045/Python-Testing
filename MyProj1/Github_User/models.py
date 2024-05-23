from django.db import models

class GitHubUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    public_repos = models.IntegerField(blank=True, null=True)
    followers = models.IntegerField(blank=True, null=True)
    following = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username


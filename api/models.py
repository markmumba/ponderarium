from django.db import models

# Create your models here.

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

# ------------------- USER MODEL -------------------


class User(models.Model):
    """Custom User model for authentication"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
    profile_picture = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


# ------------------- SOURCE MODEL -------------------
class Source(models.Model):
    """Stores authors, movies, books, or philosophers"""
    TYPE_CHOICES = [
        ('Deep Thinker', 'Deep Thinker'),
        ('Movie Scene', 'Movie Scene'),
        ('Literature', 'Literature'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


# ------------------- THEME MODEL -------------------
class Theme(models.Model):
    """Categorizes quotes into philosophical themes"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ------------------- QUOTE MODEL -------------------
class Quote(models.Model):
    """Stores quotes, monologues, and book excerpts"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    source = models.ForeignKey(
        Source, on_delete=models.CASCADE, related_name="quotes", null=True, blank=True)
    themes = models.ManyToManyField(Theme, related_name="quotes", blank=True)
    explanation = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    source_link = models.URLField(blank=True, null=True)
    submitted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="submitted_quotes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.content[:50]}..." - {self.source.name}'


# ------------------- COMMENT MODEL -------------------
class Comment(models.Model):
    """Allows users to discuss quotes"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quote = models.ForeignKey(
        Quote, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.quote}"


# ------------------- UPVOTE MODEL -------------------
class Upvote(models.Model):
    """Tracks users who upvote quotes"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="upvotes")
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="upvotes")

    class Meta:
        unique_together = ("user", "comment")  # Prevent duplicate upvotes

    def __str__(self):
        return f"{self.user.username} upvoted {self.comment}"

from rest_framework import serializers
from .models import User, Source, Theme, Quote, Comment, Upvote

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "profile_picture", "bio"]

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = "__all__"

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = "__all__"

class QuoteSerializer(serializers.ModelSerializer):
    source = SourceSerializer()
    themes = ThemeSerializer(many=True)

    class Meta:
        model = Quote
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class UpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upvote
        fields = "__all__"

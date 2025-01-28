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
    source = SourceSerializer(read_only=True)
    source_id = serializers.PrimaryKeyRelatedField(
        queryset=Source.objects.all(), write_only=True, required=False)

    themes = ThemeSerializer(read_only=True, many=True)
    theme_ids = serializers.PrimaryKeyRelatedField(
        queryset=Theme.objects.all(), many=True, write_only=True)

    submitted_by = UserSerializer(read_only=True)
    submitted_by_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Quote
        fields = [
            "id", "source", "source_id", "themes", "theme_ids", "submitted_by", "submitted_by_id",
            "content", "explanation", "image_url", "source_link", "created_at"
        ]

    def create(self, validated_data):
        source = validated_data.pop("source_id", None)
        themes = validated_data.pop("theme_ids", [])
        submitted_by = validated_data.pop("submitted_by_id")

        quote = Quote.objects.create(
            **validated_data, submitted_by=submitted_by, source=source)
        quote.themes.set(themes)
        return quote


class QuoteListSerializer(serializers.ModelSerializer):
    themes = serializers.SerializerMethodField()
    submitted_by = serializers.SerializerMethodField()

    class Meta:
        model = Quote
        fields = ['id', 'themes', 'submitted_by', 'content']

    def get_themes(self, obj):
        return [{'id': theme.id, 'name': theme.name} for theme in obj.themes.all()]

    def get_submitted_by(self, obj):
        return {'id': obj.submitted_by.id, 'username': obj.submitted_by.username}


class CommentSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['quote']

    def create(self, validated_data):
        """Create a comment without manually fetching quote_id"""
        user = validated_data.pop("user_id")
        quote = validated_data.pop("quote")

        comment = Comment.objects.create(
            **validated_data, user=user, quote=quote)
        return comment


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']

class UpvoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )
    upvotes_count = serializers.SerializerMethodField()


    class Meta:
        model = Upvote
        fields = ['id', 'user', 'user_id', 'comment', 'upvotes_count']
        read_only_fields = ['comment']

    def get_upvotes_count(self, obj):
        return Upvote.objects.filter(comment=obj.comment).count()

    def create(self, validated_data):
        user = validated_data.pop('user_id')  
        comment = self.context['comment']  

        user_instance = User.objects.get(id=user.id)  

        existing_upvote = Upvote.objects.filter(user=user_instance, comment=comment).first()
        if existing_upvote:
            raise serializers.ValidationError("User has already upvoted this comment")

        # Create the upvote
        upvote = Upvote.objects.create(user=user_instance, comment=comment)
        return upvote

class UpvoteListSerializer(serializers.ModelSerializer):
    upvotes_count = serializers.SerializerMethodField()

    class Meta:
        model = Upvote
        fields = ['id', 'upvotes_count']

    def get_upvotes_count(self, obj):
        return Upvote.objects.filter(comment=obj.comment).count()

from api.models import Movie, Comment
import api.serializers

import rest_framework.viewsets


class MovieViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = api.serializers.MovieSerializer


class CommentViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = api.serializers.CommentSerializer
    filter_fields = ('movie',)

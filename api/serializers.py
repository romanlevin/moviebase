import os

from api.models import Movie, Comment

import omdb
from rest_framework import serializers


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'year')
        read_only_fields = ('year',)

    @staticmethod
    def _fetch_from_omdb(title):
        client = omdb.OMDBClient(apikey=os.getenv('OMDB_API_KEY'))
        return client.get(title=title, media_type='movie', timeout=5.0)

    def create(self, validated_data):
        omdb_movie = self._fetch_from_omdb(validated_data['title'])
        if not omdb_movie:
            raise serializers.ValidationError(
                {
                    'title': [
                        f'{validated_data["title"]!r} does not appear to be a movie title'
                    ]
                }
            )
        return Movie.objects.create(**validated_data, year=omdb_movie['year'])


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body', 'movie', 'created_at')

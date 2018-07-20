from unittest import mock

import factory
import omdb as original_omdb
import pytest
from faker import Faker
from pytest_factoryboy import register as register_factory
from rest_framework.test import APIClient

from api import serializers

faker = Faker()


@register_factory
class MovieFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'api.Movie'

    title = factory.Faker('name')
    year = factory.LazyAttribute(lambda x: int(faker.year()))


@register_factory
class CommentFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'api.Comment'

    body = factory.Faker('paragraph')
    movie = factory.SubFactory(MovieFactory)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def omdb(monkeypatch):
    mock_omdb_client = mock.MagicMock(spec=original_omdb.OMDBClient)
    monkeypatch.setattr(original_omdb, 'OMDBClient', lambda apikey: mock_omdb_client)
    return mock_omdb_client


def test_list_movies(api_client, db, movie_factory):
    movies = api_client.get('/movies/')
    assert movies.json() == []

    first_movie = movie_factory()
    response = api_client.get('/movies/')
    movies = response.json()
    assert movies == [serializers.MovieSerializer(first_movie).data]


def test_create_movie(api_client, omdb, db, movie_factory):
    movie_to_create = movie_factory.build()
    year = movie_to_create.year
    title = movie_to_create.title

    omdb.get.return_value = {'year': str(year)}
    movie = api_client.post('/movies/', {'title': title}, format='json').json()
    assert movie['title'] == title
    assert movie['year'] == year
    assert isinstance(movie['id'], int)

    movies = api_client.get('/movies/')
    assert movies.json() == [movie]


def test_create_movie_invalid_title(api_client, omdb, db, movie_factory):
    movie_to_create = movie_factory.build()
    title = movie_to_create.title

    omdb.get.return_value = {}
    response = api_client.post('/movies/', {'title': title}, format='json')
    assert response.status_code == 400
    assert response.json()['title'] == [f'{movie_to_create.title!r} does not appear to be a movie title']


def test_list_comments(api_client, db, comment_factory):
    assert api_client.get('/comments/').json() == []

    first_comment = comment_factory()

    response = api_client.get('/comments/')
    comments = response.json()
    assert comments == [serializers.CommentSerializer(first_comment).data]


def test_create_comment(api_client, db, movie_factory):
    movie = movie_factory()
    response = api_client.post('/comments/', {'body': 'foo', 'movie': movie.pk}, format='json')
    comment = response.json()

    assert comment['body'] == 'foo'
    assert comment['movie'] == movie.pk


def test_create_comment_for_missing_movie(api_client, db, movie_factory):
    response = api_client.post('/comments/', {'body': 'foo', 'movie': 1}, format='json')
    assert response.status_code == 400
    assert 'Invalid pk' in response.json()['movie'][0]


def test_filter_comments(api_client, db, comment_factory):
    random_comments = comment_factory.create_batch(5)
    first_comment = random_comments[0]
    movie = first_comment.movie
    first_movie_comments = [first_comment] + comment_factory.create_batch(5, movie=movie)

    response = api_client.get('/comments/')
    assert len(response.json()) == 10

    response = api_client.get('/comments/', {'movie': movie.id})
    # Check for the correct number of comments
    assert len(response.json()) == 6
    # Check that all comments are associated with the first movie
    assert all(comment['movie'] == movie.pk for comment in response.json())
    # Check that all comment contents are correct
    assert set(comment.body for comment in first_movie_comments) == set(comment['body'] for comment in response.json())

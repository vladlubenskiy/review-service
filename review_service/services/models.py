from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    locked = models.BooleanField()


class Post(models.Model):
    author = models.ForeignKey(Author)
    datetime = models.DateTimeField()
    text = models.TextField()


class Request(Post):
    link_to_code = models.URLField()
    code = models.TextField()


class Review(Post):
    request_id = models.ForeignKey(Request)

# This is note to request which is shown nearby request.
# It appears like comments to code on GitHub
class Note(models.Model):
    review_id = models.ForeignKey(Review)
    text = models.TextField(max_length=500)
    label = models.IntegerField()


class Rating(models.Model):
    author = models.ForeignKey(Author)
    target = models.ForeignKey(Post)
    score = models.IntegerField(max_length=4) # 0-based score :) We are programmers


class Subscribe(models.Model):
    target = models.ForeignKey(Post)
    email = models.EmailField()


class Comment(models.Model):
    target = models.ForeignKey(Post)
    author = models.ForeignKey(Author)
    text = models.TextField(max_length=1000)
    datetime = models.DateTimeField()
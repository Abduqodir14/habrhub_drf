# import datetime
from datetime import datetime

from django.shortcuts import get_object_or_404

from apps.posts.models import Vote, Post


def vote_manager(post_id, voter):
    post = get_object_or_404(Post, id=post_id)
    vote = Vote.objects.filter(voter=voter, post=post)

    if vote.exists():
        post.rating -= 1
        post.save()
        vote.delete()

    elif not vote.exists():
        post.rating += 1
        post.save()
        Vote.objects.create(voter=voter, post=post)

    return vote


def analis_votes(post_id, date_from, date_to):
    date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
    date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
    post = Post.objects.get(id=post_id)
    return len(post.votes.filter(created_at__gte=date_from, created_at__lte=date_to))




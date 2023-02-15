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


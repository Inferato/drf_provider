import requests
from urllib.parse import urljoin
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages


def index(request):
    index_url = urljoin(settings.BLOG_BASE_URL, '/api/posts/')
    # index_url = f'{settings.HTTP_SCHEMA}{settings.BLOG_URL}/api/posts/'
    response = requests.get(index_url)
    posts = response.json()
    return render(request, 'index.html', {'posts': posts})


def post_detail(request, post_id):
    post_url = urljoin(settings.BLOG_BASE_URL, f'/api/posts/{post_id}/')
    response = requests.get(post_url)
    post = response.json()
    return render(request, 'post_detail.html', {'post': post})


def add_comment(request, post_id):
    if request.method == 'POST':
        comments_url = urljoin(settings.BLOG_BASE_URL, '/api/comments/')
        auth_token = ''
        comment_data = {'content': request.POST['content'], 'post': post_id}
        headers = {}
        if auth_token:
            headers['Authorization'] = f'Token: {auth_token}'
        response = requests.post(comments_url, data=comment_data, headers=headers)
        if response.status_code == 201:
            messages.success(request, 'Comment added successfully.')
        else:
            messages.error(request, 'Failed to add comment.')
        return redirect('post_detail', post_id=post_id)


def get_token(request):
    username = request.user.username
    response = requests.post('http://localhost:9000/get-token', data={'username': username, 'secret_key': 'test_secret_key'})
    return response.json()

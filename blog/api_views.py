from django.http import JsonResponse
from .models import Post
from django.shortcuts import get_object_or_404
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def post_list_create(request):
    if request.method == "GET":
        posts = list(Post.objects.values())
        return JsonResponse(posts, safe=False)

    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        post = Post.objects.create(
            title=data.get("title"),
            content=data.get("content"),
        )
        return JsonResponse({"id": post.id, "title": post.title, "content": post.content})
    

@csrf_exempt
def post_detail_update(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({"id": post.id, "title": post.title, "content": post.content})

    if request.method == "PUT":
        data = json.loads(request.body.decode("utf-8"))
        post.title = data.get("title", post.title)
        post.content = data.get("content", post.content)
        post.save()
        return JsonResponse({"id": post.id, "title": post.title, "content": post.content})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Blog
from .serializers import BlogSerializer
from base.api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/blogs',
        'GET /api/blogs/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getBlogs(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getBlog(request, pk):
    blog = Blog.objects.get(id=pk)
    serializer = BlogSerializer(blog, many=False)
    return Response(serializer.data)

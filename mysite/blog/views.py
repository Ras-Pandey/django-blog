from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Category, Tag
from .forms import BlogForm

# Create your views here.

def home(request):
  return render(request, 'home.html')

def blog_list(request):
    blogs = Blog.objects.all()
    category_id = request.GET.get('category')
    tag_id = request.GET.get('tag')
    if category_id:
        blogs = blogs.filter(category_id=category_id)
    if tag_id:
        blogs = blogs.filter(tags__id=tag_id)
    return render(request, 'blog_list.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog_detail.html', {'blog': blog})

def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogForm()
    return render(request, 'add_blog.html', {'form': form})
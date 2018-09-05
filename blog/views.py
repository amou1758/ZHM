import markdown
from django.shortcuts import render, get_object_or_404
from .models import *
from comments.forms import CommentForm



def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 博文详情页
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
    
                              ])
    # 创建表单实例
    form = CommentForm()
    # 获取这篇文章的所有评论
    comment_list = post.comment_set.all()
    # 获取这篇文章评论的数量
    comment_count = post.comment_set.all().count()
    
    # 将文章, 表单, 以及文章下的评论列表作为模板变量传递给  detail.html 模版
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list,
        'comment_count': comment_count,
    }
    return render(request, 'blog/detail.html', context=context)


# 归档
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 分类
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
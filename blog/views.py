import markdown
from django.shortcuts import render, get_object_or_404
from .models import *
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator

# # 该函数已被 IndexView 类视图取代
# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})
#
#
# # 博文详情页
# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.increase_views()
#     post.body = markdown.markdown(post.body,
#                                   extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                       'markdown.extensions.toc',
#
#                               ])
#     # 创建表单实例
#     form = CommentForm()
#     # 获取这篇文章的所有评论
#     comment_list = post.comment_set.all()
#     # 获取这篇文章评论的数量
#     comment_count = post.comment_set.all().count()
#
#     # 将文章, 表单, 以及文章下的评论列表作为模板变量传递给  detail.html 模版
#     context = {
#         'post': post,
#         'form': form,
#         'comment_list': comment_list,
#         'comment_count': comment_count,
#     }
#     return render(request, 'blog/detail.html', context=context)
#
#
# # 归档
# def archives(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month
#                                     ).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})
#
#
# # 分类
# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})


# 使用django封装的视图类
class IndexView(ListView):
    """
    mode: l将 model 指定为 Post，告诉 Django 我要获取的模型是 Post。
    template_name: 指定这个视图渲染的模板。
    context_object_name: 指定获取的模型列表数据保存的变量名。这个变量会被传递给模板。
    
    """
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 每页显示的文章数量
    paginate_by = 1


# 分类文章列表  ListView 类视图
class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
    
    
# 归类文章列表
class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    
    
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year, created_time__month=month)
    

class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        comment_count = self.object.comment_set.all().count()
        context.update({
            'form': form,
            'comment_list': comment_list,
            'comment_count': comment_count,
        })
        return context




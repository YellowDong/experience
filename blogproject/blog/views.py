from django.shortcuts import render, get_object_or_404
from .models import Post
import markdown

# Create your views here.

# from django.http import HttpResponse


def index(request):
    # return HttpResponse("liang shao dong huan ying nin !")
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html',
                  context={'title': 'this is a title', 'post_list': post_list})

# 使用视图类
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """在视图函数中将模板变量传递给模板是通过render函数的context参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list}),
        这里传递一个{'post_list': post_list}字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过get_context_data获得的，
        所以我们要复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去
        """
        # 首先获得父类生成的传递给模板的字典
        context = super().get_context_data(**kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        curren_page = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        left_range = []
        right_range = []

        first = False
        last = False

        left_has_more = False
        right_has_more = False

        if curren_page == 1:
            right_range =page_range[curren_page:curren_page + 2]
            if right_rang[-1] < total_pages:
                last = True
            if right_range[-1] + 1 < total_pages:
                right_has_more = True

        elif curren_page == total_pages:
            left_range =page_range[(curren_page-3) if (page_number - 3) > 0
                                   else 0:total_pages]
            if left_range[0] - 1 > 1:
                left_has_more = True
                if left_range[0] > 1:
                    first = True

        else:
            left_range = page_range[(curren_page-3) if (curren_page-3)>0
                                     else 0:curren_page-1]
            right_range = page_range[curren_page:curren_page+2]
            if right_range[-1] < total_pages -1:
                right_has_more = True
            if right_range[-1] < total_pages:
                last = True





def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  entensions=['markdown.extensions.extra',
                                              'markdown.extensions.codehilite',
                                              'markdown.extensions.toc',])
    return render(request, 'blog/detail.html', context={'post': post})

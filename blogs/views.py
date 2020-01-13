from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.views.generic import DetailView, ListView
from .models import Blog, Comments
from django.http import Http404


class BlogDetail(DetailView):
    model = Blog
    template_name = "blogs/blog.html"
    context_object_name = "blog"

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        qs = Blog.objects.filter(slug=slug)
        if qs.exists():
            instance = qs.first()
            comments = instance.blog_comments.all()[:5]
            other_blogs = Blog.objects.exclude(pk=instance.pk)
            return instance, other_blogs, comments
        return Http404

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = request.POST
            user = request.user
            blog = self.get_object()[0]
            content = data.get('comment_content')
            comment_obj = Comments.objects.create(blog=blog, content=content)
            comment_obj.user.add(user)
            comment_obj.save()
            messages.success(request, message='Posted your Comment!')
            return HttpResponseRedirect('')
        else:
            messages.error(request=request, message='Please Log In or Signup to comment!')
            return HttpResponseRedirect('', {'messages': messages.get_messages(request)}
            )


class BlogList(ListView):
    model = Blog
    template_name = 'blogs/blog_list.html'
    context_object_name = "all_blogs"
    paginate_by = 9


def blog_featured(request):
    qs = Blog.objects.all().featured()
    paginator = Paginator(qs, 9)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    return render(request, 'blogs/blog_featured_list.html', context={'blogs': blogs})


class BlogSearchView(ListView):
    template_name = "blogs/blogs_search_query.html"
    context_object_name = "search_results"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            global found
            list1, found = Blog.objects.search_for(query)
            return list1
        else:
            return Blog.objects.featured()

    def get_context_data(self, *args, **kwargs):
        context = super(BlogSearchView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        context['found'] = found
        return context


def comment_ajax(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = request.POST
            user = request.user
            pk = data.get('blogpk')
            blog = Blog.objects.get(pk=pk)
            content = data.get('comment_content')
            comment_obj = Comments.objects.create(blog=blog, content=content)
            comment_obj.user.add(user)
            comment_obj.save()
            jsondata = {
                'name': user.get_short_name(),
                'img_url': user.image.url,
                'content': content,
                'day': comment_obj.posted_time.day,
                'month': comment_obj.posted_time.month,
                'year': comment_obj.posted_time.year,
                'done': True,
            }
            messages.success(request, message='Posted your Comment!')
            if request.is_ajax():
                return JsonResponse(jsondata)
            return HttpResponseRedirect('')
        else:
            if request.is_ajax():
                return JsonResponse({'message': 'Please Log in or signup to proceed', 'done': False})
            messages.error(request=request, message='Please Log In or Signup to comment!')
            return HttpResponseRedirect('', {'messages': messages.get_messages(request)})


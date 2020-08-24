from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, TemplateView, FormView
from blog.models import *
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, \
    TodayArchiveView
from django.db.models import Q

from blog.forms import PostSearchForm

from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin
from django.utils import timezone
from django.http import FileResponse
import os
from django.conf import settings

class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context


class PostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by = 2


class PostDV(DetailView):
    model = Post
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # post = self.get_object()
        post = self.get_object()
        post.read_cnt += 1
        post.save()
        return context


class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_dt'


class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_dt'
    # make_object_list = True


class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'modify_dt'
    month_format = '%m'


class PostDAV(DayArchiveView):
    model = Post
    date_field = 'modify_dt'
    month_format = '%m'


class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'modify_dt'
    month_format = '%m'


class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = 'blog/post_search.html'

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']
        post_list = Post.objects.filter(Q(title__icontains=searchWord) |
                                        Q(description__icontains=searchWord) |
                                        Q(content__icontains=searchWord)).distinct()
        context = {}
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = post_list

        return render(self.request, self.template_name, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tags']
    initial = {'slug': 'auto-filling-do-not-input'}
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.modify_dt = timezone.now()
        #return HttpResopnseRedirect(self.get_success_url())
        response = super().form_valid(form)
        files = self.request.FILES.getlist("files")
        for file in files:
            attach_file = PostAttachFile(post=self.object, filename=file.name, size=file.size,
                                         content_type=file.content_type, upload_file=file)
            attach_file.save()
        return response


class PostUpdateView(OwnerOnlyMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tags']
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.modify_dt = timezone.now()
        # return HttpResopnseRedirect(self.get_success_url())
        response = super().form_valid(form)
        check_val = self.request.POST.getlist("delete-check")
        for delfile in check_val:
            targets = PostAttachFile.objects.get(id=int(delfile))
            filepath = os.path.join(settings.MEDIA_ROOT, str(targets.upload_file))
            os.remove(filepath)
            targets.delete()

        files = self.request.FILES.getlist("files")
        for file in files:
            attach_file = PostAttachFile(post=self.object, filename=file.name, size=file.size,
                                         content_type=file.content_type, upload_file=file)
            attach_file.save()

        return response


class PostDeleteView(OwnerOnlyMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')


class HomeView(ListView):
    template_name = 'home.html'
    model = Post
    nowtime = timezone.now()
    context_object_name = 'posts'
    paginate_by = 2
    def get_queryset(self):
        return Post.objects.filter(Q(modify_dt__year=self.nowtime.year) &
                                    Q(modify_dt__month=self.nowtime.month) &
                                    Q(modify_dt__day=self.nowtime.day))


def download(request, id):
    file = PostAttachFile.objects.get(id=id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(file.upload_file))

    return FileResponse(open(file_path, 'rb'))

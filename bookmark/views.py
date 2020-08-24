from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView,CreateView, UpdateView, DeleteView
from bookmark.models import Bookmark
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin

class BookmarkLV(ListView):
    model = Bookmark
    context_object_name = 'bookmark_list'


class BookmarkDV(DetailView):
    model = Bookmark
    context_object_name = 'bookmark_detail'


class BookmarkCreateView(LoginRequiredMixin, CreateView):
    model = Bookmark
    fields = ['title', 'url']
    success_url = reverse_lazy('bookmark:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class BookmarkChangeLV(LoginRequiredMixin, ListView):
    template_name = 'bookmark/bookmark_change_list.html'
    def get_queryset(self):
        return Bookmark.objects.filter(owner=self.request.user)


class BookmarkUpdateView(OwnerOnlyMixin, UpdateView):
    model = Bookmark
    fields = ['title', 'url']
    success_url = reverse_lazy('bookmark:index')


class BookmarkDeleteView(OwnerOnlyMixin, DeleteView):
    model = Bookmark
    template_name = "bookmark/bookmark_delete.html"
    success_url = reverse_lazy('bookmark:index')


def go_to_main(request):
    return render(request, "bookmark/bookmark_main.html")


def index(request):
    bookmark_list = Bookmark.objects.all()
    context = {'bookmark_list': bookmark_list} #must be dict
    return render(request, "bookmark/bookmark_list.html", context)


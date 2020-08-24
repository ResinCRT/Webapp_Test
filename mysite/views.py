from django.views.generic import TemplateView, ListView
from django.views.generic import CreateView, TodayArchiveView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from blog.models import Post

from django.contrib.auth.views import PasswordChangeView




from django.contrib.auth.mixins import AccessMixin
from django.views.defaults import permission_denied
import datetime

class HomeView(TodayArchiveView):
    template_name = 'home.html'
    model = Post
    date_field = 'modify_dt'
    allow_empty = True




#--- User Creation
class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')

class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'

class OwnerOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "Owner only can update/ delete the object"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.owner:
            self.handle_no_permission()
        return super().get(request, *args, **kwargs)

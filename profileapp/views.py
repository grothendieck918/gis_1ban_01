from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from profileapp.decorators import profile_ownership_required
from profileapp.forms import ProfileCreationForm
from profileapp.models import Profile

@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
# 이제는 정상적으로 로그인한유저만 프로필생성뷰로 접근가능함
class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileCreationForm
    # success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'profileapp/create.html'
    
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('accountapp:detail', kwargs={'pk': self.object.user.pk })
    # kwarg로 pk를 넘겨준다

@method_decorator(profile_ownership_required, 'get')
@method_decorator(profile_ownership_required, 'post')
class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileCreationForm
    context_object_name = 'target_profile'
    # success_url = reverse_lazy('accountapp:hello_world') method를 이용해 동적으로 받을거임
    template_name = 'profileapp/update.html'
    # view를 만들고 어느주소로 접근해야할지 urls.py작성하러가

    def get_success_url(self):
        return reverse('accountapp:detail', kwargs={'pk' : self.object.user.pk})
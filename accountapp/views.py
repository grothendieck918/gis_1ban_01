from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
# ctrl + b
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin

from accountapp.decorators import account_ownership_required
from accountapp.forms import AccountCreationForm
from accountapp.models import HelloWorld


# @login_required(login_url = reverse_lazy('accountapp:login')) #기본적으로 accountapp의 앱이름에 login 으로 이동되게 적혀있어서 생략가능
from articleapp.models import Article


@login_required
def hello_world(request):

    # if request.user.is_authenticated:
        # request를 보내는 그 user가 로그인이 되어있다면

        if request.method == 'POST':
            temp = request.POST.get('hello_world_input')
            new_hello_world = HelloWorld()
            new_hello_world.text = temp
            new_hello_world.save()

            return HttpResponseRedirect(reverse('accountapp:hello_world'))

            # hello_world_list = HelloWorld.objects.all()
            # return render(request, 'accountapp/hello_world.html', context={'hello_world_list': hello_world_list})
        else:
            hello_world_list = HelloWorld.objects.all()
            return render(request, 'accountapp/hello_world.html', context={'hello_world_list':hello_world_list})
    # else:
    #     return HttpResponseRedirect(reverse('accountapp:login'))


class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    # success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/create.html'

    def get_success_url(self):
        return reverse('accountapp:detail', kwargs={'pk': self.object.pk})
    # 아까 object는 target profile이어엇지만 지금은 targetuser라 바로 pk

class AccountDetailView(DetailView, MultipleObjectMixin):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'

    paginate_by = 20

    def get_context_data(self, **kwargs):
        article_list = Article.objects.filter(writer=self.object)
        return super().get_context_data(object_list=article_list, **kwargs)


has_ownership = [login_required, account_ownership_required]

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
# 이 두개로는 로그인의 유무만 확인가능하므로 user와 targetuser가 동일한것도확인해줘야함
class AccountUpdateView(UpdateView):
    model = User
    form_class = AccountCreationForm
    context_object_name = 'target_user'
    # success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/update.html'

    def get_success_url(self):
        return reverse('accountapp:detail', kwargs={'pk': self.object.pk})


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/delete.html'

    # def get(self, request, *args, **kwargs):
    #     if request.user.is_authenticated and self.get_object() == request.user:
    #         # 안에있는 계정객체와 리퀘스트를 보낸 유저와 동일한지 확인
    #         return super().get(request, *args, **kwargs)
    #     else:
    #         return HttpResponseForbidden()
    #
    # def post(self, request, *args, **kwargs):
    #     if request.user.is_authenticated and self.get_object() == request.user:
    #         return super().post(request, *args, **kwargs)
    #     else:
    #         return HttpResponseForbidden()


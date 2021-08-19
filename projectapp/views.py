from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.list import MultipleObjectMixin

from articleapp.models import Article
from projectapp.forms import ProjectCreationForm
from projectapp.models import Project
from subscribeapp.models import Subscription


@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = 'projectapp/create.html'

    def get_success_url(self):
        return reverse('projectapp:detail', kwargs={'pk': self.object.pk})
    # self.object 크리에이트뷰에서만들어진 객체


class ProjectDetailView(DetailView, MultipleObjectMixin):
    # 다수의 객체를 사용할수있게하는 멀티플오브젝트믹스인
    model = Project
    context_object_name = 'target_project'
    template_name = 'projectapp/detail.html'

    paginate_by = 20

    def get_context_data(self, **kwargs):
        user = self.request.user
        project = self.object

        subscription = Subscription.objects.filter(user=user,
                                                   project=project)

        if subscription.exists():
            subscription = 1
        else:
            subscription = None

        article_list = Article.objects.filter(project=self.object)
        # 해당프로젝트의 게시글만 필터링
        return super().get_context_data(object_list=article_list,
                                        subscription=subscription,
                                        **kwargs)


class ProjectListView(ListView):
    model = Project
    context_object_name = 'project_list'
    # target의 list가 아니라 project의 리스트를 받는다는 의미로
    template_name = 'projectapp/list.html'
    paginate_by = 20
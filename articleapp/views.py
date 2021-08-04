from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView

from articleapp.forms import ArticleCreationForm
from articleapp.models import Article


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleCreationForm
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'articleapp/create.html'

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)


class ArticleDetailView(DetailView):
    model = Article
    # html에서 어떤객체를통해 오브젝트를 이동할건지
    context_object_name = 'target_article'
    template_name = 'articleapp/detail.html'

class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleCreationForm
    context_object_name = 'target_article'
    template_name = 'articleapp/update.html'

    # 특성 success_url = 로가기위해선 메소드사용
    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk': self.object.pk})

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView

from articleapp.models import Article
from likeapp.models import LikeRecord

@method_decorator(login_required, 'get')
class LikeArticleView(RedirectView):

    def get(self, request, *args, **kwargs):
        user = request.user
        # 요청을 보낸 유저를 저장
        article = Article.objects.get(pk=kwargs['article_pk'])
        # 어떤 게시글에 좋아요를 눌렀는지

        likeRecord = LikeRecord.objects.filter(user=user,
                                               article=article)
        if likeRecord.exists():
            return HttpResponseRedirect(reverse('articleapp:detail', kwargs={'pk': kwargs['article_pk']}))
        else:
            LikeRecord(user=user, article=article).save()

        article.like +=1
        article.save()

        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('articleapp:detail', kwargs={'pk': kwargs['article_pk']})
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView

from articleapp.models import Article
from likeapp.models import LikeRecord


@transaction.atomic #db 를 엮어줘서 하나가실패하면 다른것도실패시키는것
def db_transaction(user, article):
    likeRecord = LikeRecord.objects.filter(user=user,
                                           article=article)

    article.like += 1
    article.save()

    if likeRecord.exists():
        # 좋아요 반영 X
        # django.contrib.messages
        raise ValidationError('좋아요가 이미 존재합니다.')
    else:
        LikeRecord(user=user, article=article).save()



@method_decorator(login_required, 'get')
class LikeArticleView(RedirectView):

    def get(self, request, *args, **kwargs):
        user = request.user
        # 요청을 보낸 유저를 저장
        article = Article.objects.get(pk=kwargs['article_pk'])
        # 어떤 게시글에 좋아요를 눌렀는지
        try:
            db_transaction(user, article)
            # 좋아요 반영 O
            messages.add_message(request, messages.SUCCESS, '좋아요가 반영되었습니다.')
        except ValidationError:
            messages.add_message(request, messages.ERROR, '좋아요는 한번만 가능합니다.')
            return HttpResponseRedirect(reverse('articleapp:detail', kwargs={'pk': kwargs['article_pk']}))

        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('articleapp:detail', kwargs={'pk': kwargs['article_pk']})
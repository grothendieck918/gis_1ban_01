from django.http import HttpResponseForbidden
from django.contrib.auth.models import User


def account_ownership_required(func):
    def decorated(request, *args, **kwargs):
        target_user = User.objects.get(pk=kwargs['pk'])
        # User라는 오브젝트를 데이터베이스에서 꺼내옴
        if target_user == request.user:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    return decorated






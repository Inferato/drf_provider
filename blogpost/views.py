from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

@csrf_exempt
@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def custom_token_obtaining(request):
    username = request.POST.get('username')
    secret_key = request.POST.get('secret_key')

    if secret_key == settings.BLOG_SECRET_KEY:
        user, _ = User.objects.get_or_create(username=username)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

        



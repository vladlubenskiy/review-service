from django.http import HttpResponse
from review_service.oauth.google.authentication import authorized_only

@authorized_only
def MainPage(request):
    return HttpResponse("Hello world!")


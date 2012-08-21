from django.http import HttpResponse
from review_service.oauth.google.authentication import authorized_only
from services.models import Author

@authorized_only
def MainPage(request):
    try:
        author = Author.objects.get(email=request.session["user_info"]["email"])
    except Author.DoesNotExist:
        return HttpResponse(status=500)

    return HttpResponse("Hello, " + author.name + " &lt;" + author.email + "&gt;!")


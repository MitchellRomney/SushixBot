import requests

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def followers(request):
    print('Received request on /twitch/followers endpoint.')
    if request.GET["hub.challenge"]:
        print(f'Got challenge key: {request.GET["hub.challenge"]}')
        return HttpResponse(request.GET["hub.challenge"], status=200)
    return HttpResponse(status=204)

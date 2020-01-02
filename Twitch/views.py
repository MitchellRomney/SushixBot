import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def followers(request):
    print(f'Received /followers {request.method} request!')

    if request.method == 'GET':
        if "hub.challenge" in request.GET:
            return HttpResponse(request.GET["hub.challenge"], status=200)

    elif request.method == 'POST':
        body = json.loads(request.body)
        if "data" in body:
            print(body["data"])
            print(body["data"][0])
            payload = body["data"][0]
            print(f'New follower: {payload["from_name"]}, Twitch ID: {payload["from_id"]}')

    return HttpResponse(status=204)

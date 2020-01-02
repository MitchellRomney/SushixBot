from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def followers(request):
    if request.GET["hub.challenge"]:
        return HttpResponse(request.GET["hub.challenge"], status=200)

    elif request.method == 'POST':
        if "data" in request.body:
            payload = request.body["data"][0]
            print(f'New follower: {payload["from_name"]}, Twitch ID: {payload["from_id"]}')

    return HttpResponse(status=204)

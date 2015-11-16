from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pubnub import Pubnub

from api_server import settings
from geofencing_api.models import Graph
from geofencing_api.views import user_base

__author__ = 'dipap'


# pubnub instance -- singleton
pubnub = Pubnub(publish_key=settings.PUBNUB_PUBLISH_KEY,
                subscribe_key=settings.PUBNUB_SUBSCRIBE_KEY,
                ssl_on=True)


@csrf_exempt
def graphs(request):
    if request.method == 'GET':
        return JsonResponse([g.to_json() for g in Graph.objects.all()], safe=False)

    elif request.method == 'POST':
        # get graph options
        if 'lat' not in request.POST or 'lng' not in request.POST:
            return JsonResponse({'error': 'lat,lng are required'}, status=403)
        x = float(request.POST.get('lat'))
        y = float(request.POST.get('lng'))
        label = request.POST.get('label', None)

        # get list of users in the graph
        uid_list = ','.join([u.pk for u in user_base.in_group(x, y)])

        # create the graph
        g = Graph.objects.create(lat=x, lng=y, label=label, uid_list=uid_list)

        return JsonResponse(g.to_json())

    else:
        # note: replacing & deleting graph list not supported
        return JsonResponse({'error': 'Method %s not supported' % request.method}, status=403)


@csrf_exempt
def graph(request, pk):
    try:
        g = Graph.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Node with id %s not found' % pk}, status=404)

    if request.method == 'GET':
        # return graph description
        return JsonResponse(g.to_json())

    elif request.method == 'DELETE':
        # delete graph
        g.delete()

        return JsonResponse({}, status=204)

    else:
        # graphs can't be updated
        return JsonResponse({'error': 'Method %s not supported' % request.method}, status=403)


@csrf_exempt
def send_message(request, pk):
    """
    Send a new message to all users in graph
    """
    if request.method == 'POST':
        # find the graph
        try:
            g = Graph.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Node with id %s not found' % pk}, status=404)

        # get the message
        message = request.POST.get('message', '')
        if not message:
            return JsonResponse({'error': 'message can\'t be empty'}, status=404)

        # push it to all users
        for uid in g.uid_list.split(','):
            pubnub.publish(channel=uid, message=message)

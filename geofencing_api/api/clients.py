import uuid

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from geofencing_api.views import user_base

__author__ = 'dipap'


@csrf_exempt
def clients(request):
    if request.method == 'POST':
        # client registering
        pk = uuid.uuid4()
        return JsonResponse({'message': 'Registration successful', 'id': pk}, status=201)

    else:
        return JsonResponse({'error': 'Method %s not supported' % request.method}, status=403)


@csrf_exempt
def client(request, pk):
    if request.method == 'POST':
        try:
            x = float(request.POST.get('lat'))
            y = float(request.POST.get('lng'))
        except TypeError:
            return JsonResponse({'error': 'lat,lng coordinate arguments are required' % request.method}, status=403)

        user = user_base.get_user(pk)
        user.update(x, y)

        return JsonResponse({})

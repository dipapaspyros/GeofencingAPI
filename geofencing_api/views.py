from django.http import JsonResponse
from django.shortcuts import render

import threading
from geofencing_api.client.user import UserBase

# create user base
from api_server.settings import DEBUG

if DEBUG:
    # simulate users
    user_base = UserBase(init_n_of_users=2000)

    # manager moving
    t = threading.Thread(target=user_base.iteration)
    t.start()
else:
    user_base = UserBase()

# Create your views here.
def get_users(request):
    return JsonResponse([u.to_json() for u in user_base.users], safe=False)


def get_users_in_group(request):
    x = float(request.GET.get('lat'))
    y = float(request.GET.get('lng'))

    return JsonResponse([u.to_json() for u in user_base.in_group(x, y)], safe=False)


def main_page(request):
    return render(request, 'index.html')

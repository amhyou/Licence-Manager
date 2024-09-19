from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Licence, Device
from datetime import timedelta, date
import json, uuid

@csrf_exempt
def check_licence(request: HttpRequest):
    if request.method != "POST":
        data = data = {
            'msg': 'method not allowed',
            'status': 'ko'
        }
        return JsonResponse(data)
    body = json.loads(request.body)
    print(body)
    # check if mac and licence are included in the request body
    key = body.get("licence")
    mac = body.get("mac")
    if key is None or mac is None:
        data = data = {
            'msg': 'body is not correct',
            'status': 'ko'
        }
        return JsonResponse(data)

    # check if the licence exists
    licence: Licence = Licence.objects.filter(key=key).first()
    if licence is None:
        data = data = {
            'msg': 'not existing licence',
            'status': 'ko'
        }
        return JsonResponse(data)

    # check if the licence is not expired yet
    if licence.expiration_date < date.today():
        data = data = {
            'msg': 'licence expired',
            'status': 'ko'
        }
        return JsonResponse(data)
    
    # check if the licence is still active
    if licence.status != "active":
        data = data = {
            'msg': 'licence is not active',
            'status': 'ko'
        }
        return JsonResponse(data)

    # check if the licence has already maximum devices
    mac_addresses = Device.objects.filter(licence=licence).values_list('mac', flat=True)
    print(mac_addresses)
    if mac in mac_addresses:    
        data = {
            'msg': 'mac address valid',
            'status': 'ok'
        }
        return JsonResponse(data)
    elif len(mac_addresses) < 3:
        Device.objects.create(licence=licence, mac=mac)
        data = {
            'msg': 'mac address added',
            'status': 'ok'
        }
        return JsonResponse(data)
    else:
        data = {
            'msg': 'licence has full devices',
            'status': 'ko'
        }
        return JsonResponse(data)


@csrf_exempt
def add_licence(request: HttpRequest):
    if request.method != "POST":
        data = data = {
            'msg': 'method not allowed',
            'status': 'ko'
        }
        return JsonResponse(data)

    licence = Licence.objects.create(key=str(uuid.uuid4()), expiration_date=date.today()+timedelta(days=30))

    data = {
        'licence_key': licence.key,
        'days': (licence.expiration_date - licence.issued_date).days,
    }

    return JsonResponse(data)
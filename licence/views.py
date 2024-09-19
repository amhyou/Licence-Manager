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
    body = json.loads(request.body)   # { "licence": "qsfdsdfs",  }
    print(body)
    data = {
        'msg': '123456',
        'status': 'ok'
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

    licence = Licence.objects.create(key=str(uuid.uuid4()),expiration_date=date.today()+timedelta(days=30))

    data = {
        'licence': licence.key,
        'days': (licence.expiration_date - licence.issued_date).days,
    }

    return JsonResponse(data)
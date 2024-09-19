from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def check(request: HttpRequest):
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
def add(request: HttpRequest):
    if request.method != "POST":
        data = data = {
            'msg': 'method not allowed',
            'status': 'ko'
        }
        return JsonResponse(data)
    body = json.loads(request.body)
    print(body)
    data = {
        'msg': '123456',
        'status': 'ok'
    }
    return JsonResponse(data)
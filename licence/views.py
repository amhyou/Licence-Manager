from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status

from .models import Licence, Device
from datetime import date


@swagger_auto_schema(
    operation_id="check_licence",
    method='POST',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'licence': openapi.Schema(type=openapi.FORMAT_UUID, description='Licence Key'),
            'mac': openapi.Schema(type=openapi.TYPE_STRING, description='Mac Address'),
        },
    ),
    responses={
        200: openapi.Response(description='Valid licence', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={'msg': openapi.Schema(type=openapi.TYPE_STRING), 'status': openapi.Schema(type=openapi.TYPE_STRING)})),
        400: openapi.Response(description='Invalid licence'),
        500: openapi.Response(description='Internal server error'),
    }
)
@api_view(['POST'])
def check_licence(request):
    body = request.data
    print(body)
    # check if mac and licence are included in the request body
    key = body.get("licence")
    mac = body.get("mac")
    if key is None or mac is None:
        data = data = {
            'msg': 'body is not correct',
            'status': 'ko'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    # check if the licence exists
    try:
        licence: Licence = Licence.objects.filter(key=key).first()
    except Exception as ex:
        print(ex)
        return Response({'msg': 'Internal server error', 'status': 'ko',}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if licence is None:
        data = data = {
            'msg': 'not existing licence',
            'status': 'ko'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    # check if the licence is not expired yet
    if licence.expiration_date < date.today():
        data = data = {
            'msg': 'licence expired',
            'status': 'ko'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    # check if the licence is still active
    if licence.status != "active":
        data = data = {
            'msg': 'licence is not active',
            'status': 'ko'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    # check if the licence has already maximum devices
    try:
        mac_addresses = Device.objects.filter(licence=licence).values_list('mac', flat=True)
    except Exception as ex:
        print(ex)
        return Response({'msg': 'Internal server error', 'status': 'ko',}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    print(mac_addresses)
    if mac in mac_addresses:    
        data = {
            'msg': 'mac address valid',
            'status': 'ok'
        }
        return Response(data, status=status.HTTP_200_OK)
    elif len(mac_addresses) < 3:
        try:
            Device.objects.create(licence=licence, mac=mac)
        except Exception as ex:
            print(ex)
            return Response({'msg': 'Internal server error', 'status': 'ko',}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = {
            'msg': 'mac address added',
            'status': 'ok'
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {
            'msg': 'licence has full devices',
            'status': 'ko'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
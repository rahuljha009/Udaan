from enum import Flag
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from limitedTimeDeal import serializers, models
from datetime import datetime, timedelta
import uuid

# Create your views here.

DEFAULT_TIME_HOURS = 2
class UserProfileApiView(APIView):

    serializer_class = serializers.UserProfileSerializer

    def post(self, request) -> Response:

        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            name = user_serializer.validated_data.get('name')
            return Response({'message': f'Welcome {name}, Account created successfully'})
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DealApiView(APIView):
    serializer_class = serializers.DealSerializer
    
    def post(self, request) -> Response:

        user = request.data['user']

        try:
            seller = models.UserProfile.objects.get(id=user)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        start_time = datetime.now()
        end_time_hour = DEFAULT_TIME_HOURS
        if 'start_time' in request.data:
            date_format_str = '%d/%m/%Y %H:%M'
            time_str = request.data.get('start_time') #start time in dd/mm/YYYY HH:MM format
            start_time = datetime.strptime(time_str,date_format_str)
        
        if 'end_time' in request.data:
            end_time_hour = request.data.get('end_time') #number of hour after start time
        else:
            end_time_hour = DEFAULT_TIME_HOURS
        end_time = start_time + timedelta(hours=end_time_hour)
        
        data = request.data
        data._mutable = True

        data['start_time'] = start_time
        data['end_time'] = end_time
        data['user'] = user
        
        deal_serializer = self.serializer_class(data=data)
        
        if deal_serializer.is_valid():
            deal_serializer.save()
            seller_id = deal_serializer.data.get('user')
            return Response({'message': f'Deal created successfully by seller-id: {seller_id}'})
        return Response(deal_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class EndDeal(APIView):
    model = models.Deal

    def put(self, request, deal_id) -> Response:

        data = request.data
        data._mutable = True
        data['deal_id'] =deal_id
        if 'isEnd' not in data:
            data['isEnd'] = True
        deal = self.model.objects.get(id=deal_id)
        res = deal.update(data)
        return Response(res)
        

class UpdateDeal(APIView):
    model = models.Deal

    def put(self, request, deal_id) -> Response:

        data = request.data
        data._mutable = True
        data['deal_id'] =deal_id
        if 'price' in data or 'end_time' in data:
            deal = self.model.objects.get(id=deal_id)
            res = deal.update(data)
            return Response(res)
        return Response({'message': 'Wrong Input'})
        
class ClaimDealApiView(APIView):

    model = models.ClaimDeal

    def post(self, request, deal_id) -> Response:

        data = request.data
        data._mutable = True
        buyer_id = data['user']
        buyer = models.UserProfile.objects.get(id=buyer_id)
        deal = models.Deal.objects.get(id=deal_id)
        now_time  = datetime.now()
        end_time_raw = deal.end_time 
        end_time = end_time_raw.replace(tzinfo=None)
        diff = now_time - end_time

        if not buyer:
            return Response("No valid buyer")
        if deal.isEnd:
            return Response("Deal is End")
        if (now_time>end_time) or (deal.quantity==0):
            data['isEnd'] = True
            res = deal.update(data)
            return Response("Deal is End")
        buyer_list_obj = self.model.objects.filter(deal_id=deal_id)
        buyer_uuid = str(uuid.UUID(buyer_id))
        for ele in buyer_list_obj:
            ele_id = str(ele.user_id)
            if (buyer_uuid == ele_id):
                return Response("Buyer has already bought")
        
        data['deal_id'] =deal_id
        data['claim_deal'] = True

        buyers = []
        buyers.append(buyer)
        obj = self.model()
        obj.deal = deal
        obj.user= buyer
        res = obj.save()
        res2 = deal.update(data)
        return Response(f"{res}. {res2}")
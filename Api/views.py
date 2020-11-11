from django.http import request
from django.shortcuts import render
from rest_framework import status,generics,permissions
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter,OrderingFilter
from .models import Comment,Customer,User,Data
from .serializers import CommentSerializer,CustomerSerializer,GoogleSocialAuthSerializer,UserSerializer,DataSerializer
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['GET', ])
def api_list_allcustomer_view(request):
    customer=Customer.objects.all()
    serializer=CustomerSerializer(customer,many=True)
    return Response(serializer.data)

    
@api_view(['GET', ])
def api_list_customer_view(request,slug):
    customer=Customer.objects.filter(assignedto_id=slug)
    serializer=CustomerSerializer(customer,many=True)
    return Response(serializer.data)

@api_view(['GET', ])
def api_detail_customer_view(request,slug):
    customer=Customer.objects.get(id=slug)
    serializer=CustomerSerializer(customer)
    return Response(serializer.data)


@api_view(['GET', ])
def api_detail_employee_view(request,slug):
    employee = User.objects.get(id=slug)
    serializer=UserSerializer(employee)
    return Response(serializer.data)


@api_view(['GET','PUT'])
def api_detail_data_view(request,slug):
    data = Data.objects.get(employee_id=slug)
    if request.method == 'GET':
        serializer=DataSerializer(data)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer=DataSerializer(data,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)


@api_view(['GET', ])
def api_all_customer_comment_view(request,slug):
    comment=Comment.objects.filter(customer_id=slug)
    serializer=CommentSerializer(comment,many=True)
    return Response(serializer.data)

@api_view(['GET', ])
def api_customer_filter_label_view(request,slug):
    customer=Customer.objects.filter(label=slug)
    serializer=CustomerSerializer(Customer,many=True)
    return Response(serializer.data)

@api_view(['GET', ])
def api_customer_filter_team_view(request,slug):
    customer=Customer.objects.filter(team=slug)
    serializer=CustomerSerializer(Customer,many=True)
    return Response(serializer.data)

@api_view(['GET', ])
def api_customer_filter_firsttag_view(request,slug):
    customer=Customer.objects.filter(firsttag=slug)
    serializer=CustomerSerializer(Customer,many=True)
    return Response(serializer.data)

class OrderedList(generics.ListAPIView):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    filter_backends=(OrderingFilter,)

@api_view(['POST', ])
def api_create_customer_comment_view(request,slug):
    serializer=CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(customer_id=slug)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def api_update_employee_view(request,slug):
    employee= User.objects.get(id=slug)
    if request.method == 'PUT':
        serializer= UserSerializer(employee,data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

@api_view(['POST', ])
def api_create_customer_view(request,slug):
    serializer=CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(assignedto_id=slug)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT','DELETE' ])
def api_update_customer_view(request,slug):
    customer=Customer.objects.all(id=slug)
    if request.method == 'PUT':
        
        serializer=CustomerSerializer(customer,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class GoogleSocialAuthView(generics.GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
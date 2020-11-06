from django.http import request
from django.shortcuts import render
from rest_framework import status,generics,permissions
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter,OrderingFilter
from .models import Comment,Customer,User
from .serializers import CommentSerializer,CustomerSerializer,GoogleSocialAuthSerializer,UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['GET', ])
def api_list_allcustomer_view(request):
    customer=Customer.objects.all()
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


@api_view(['POST', ])
def api_update_employee_comment_view(request,slug):
    employee= User.objects.get(id=slug)
    serializer= UserSerializer(employee,data=request.data)
    data={}
    if serializer.is_valid():
        data["success"]="update successful"
        return  Response(data=data)

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def api_create_customer_view(request,slug):
    serializer=CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(assignedto_id=slug)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)







class GoogleSocialAuthView(generics.GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)
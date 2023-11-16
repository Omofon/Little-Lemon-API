from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework import authentication, permissions, throttling
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .models import *
from .serializers import *

# Create your views here.


# class MultipleUsers(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser]
#     throttle_classes = [
#         throttling.AnonRateThrottle,
#         throttling.UserRateThrottle,
#     ]

#     def get(self, request, format=None):
#         usernames = [user.username for user in User.objects.all().order_by("id")]
#         return Response(usernames, 200)


# class SingleUser(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser]
#     throttle_classes = [
#         throttling.AnonRateThrottle,
#         throttling.UserRateThrottle,
#     ]

#     def get(self, request, pk=None):
#         if pk:
#             userData = User.objects.get(pk=pk)
#         else:
#             userData = []

#         return Response(userData.username, 200)

#     def put(self, request, pk=None):
#         return Response({"title": request.data.get("username")}, 200)


# class UserView(viewsets.ViewSet):
#     def list(self, request):
#         return Response({"message": "All Users"}, 200)

#     def create(self, request):
#         return Response({"message": "Creating a user"}, 200)

#     def update(self, request, pk=None):
#         user = User.objects.get(pk=pk)
#         return Response({"message": "Updating User with pk"})

#     def retrieve(self, request, pk=None):
#         return Response({"message": "Displaying User " + str(pk)}, 200)


# def UsernameFormView(request):
#     form = UsernameForm(request.POST)
#     if form.is_valid():
#         form.save()
#     context = {"form": form}

#     return render(request, "username.html", context)


# @api_view(["GET", "POST"])
# def MultiPersons(request):
#     if request.method == "GET":
#         items = Person.objects.select_related("username").all()

#         firstNameFilter = request.query_params.get("firstname")
#         lastNameFilter = request.query_params.get("lastname")
#         ageFilter = request.query_params.get("age")

#         search = request.query_params.get("search")
#         ordering = request.query_params.get("ordering")

#         perpage = request.query_params.get("perpage", default=2)
#         page = request.query_params.get("page", default=1)

#         if firstNameFilter:
#             items = items.filter(first_name=firstNameFilter)
#         elif lastNameFilter:
#             items = items.filter(last_name=lastNameFilter)
#         if ageFilter:
#             items = items.filter(age=ageFilter)

#         if search:
#             items = items.filter(first_name__icontains=search)

#         if ordering:
#             ordering_fields = ordering.split(",")
#             items = items.order_by(*ordering_fields)

#         paginator = Paginator(items, per_page=perpage)
#         try:
#             items = paginator.page(number=page)
#         except EmptyPage:
#             items = []
#         serialized_item = PersonSerializer(items, many=True)
#         return Response(serialized_item.data, status=200)
#     elif request.method == "POST":
#         serialized_item = PersonSerializer(data=request.data)
#         serialized_item.is_valid(raise_exception=True)
#         serialized_item.save()
#         return Response(serialized_item.data, status.HTTP_201_CREATED)


# @api_view()
# def GetSinglePerson(request, id):
#     sb = get_object_or_404(Person, pk=id)
#     serialized_item = PersonSerializer(sb)

#     return Response(serialized_item.data, 200)


# class PersonViewSet(viewsets.ModelViewSet):
#     queryset = Person.objects.all()
#     serializer_class = PersonSerializer


# @api_view()
# @permission_classes([IsAuthenticated])
# def secret(request):
#     return Response({"message": "some secret message"})


# @api_view()
# @permission_classes([IsAuthenticated])
# def manager_view(request):
#     if request.user.groups.filter(name="Manager").exists():
#         return Response({"message": "you fit see this ba?"}, 200)
#     else:
#         return Response({"message": "goan regista as manager"}, 403)


# class ManagerView(APIView):
#     def isManager(self, request):
#         if request.user.groups.filter(name="Manager").exists():
#             return True
#         else:
#             return False

#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [isManager]

#     def get(self, request, format=None):
#         return Response({"message": "this is the manager view"})


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    ordering_fields = ["price", "inventory"]
    filterset_fields = ["price", "inventory"]
    search_fields = ["title"]

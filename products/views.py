from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from products.mixins import SerializerByMethodMixin
from products.models import Product
from products.permissions import IsSellerAndOwnerOrReadOnly, IsSellerOrReadOnly
from products.serializers import CreateProductSerializer, ListProductSerializer


class ListCreateProductView(SerializerByMethodMixin ,generics.ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsSellerOrReadOnly]

    queryset = Product.objects.all()
    serializer_map = {
        "GET": ListProductSerializer,
        "POST": CreateProductSerializer,
    }

    def perform_create(self, serializer):
        return serializer.save(seller=self.request.user)

class RetrieveUpdateProductView(SerializerByMethodMixin, generics.RetrieveUpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsSellerAndOwnerOrReadOnly]

    queryset = Product.objects.all()
    queryset = Product.objects.all()
    serializer_map = {
        "GET": ListProductSerializer,
        "PATCH": CreateProductSerializer,
    }

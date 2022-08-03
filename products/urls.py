from django.urls import include, path

from products.views import ListCreateProductView, RetrieveUpdateProductView

urlpatterns = [
    path('products/', ListCreateProductView.as_view()),
    path('products/<pk>/', RetrieveUpdateProductView.as_view())
]

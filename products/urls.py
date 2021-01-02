from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    # Product detail specifies int so when we go to /product/add it will
    # not try to look for a product called 'add' and will allow the add/
    # view to be called instead as django will use the first url it finds
    # a matching pattern for.
]

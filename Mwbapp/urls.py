from django.urls import path
from Mwbapp import views


urlpatterns = [
    # Auth
    path('register/',views.RegisterView.as_view(),name = 'register'),
    path('login/',views.LoginView.as_view(),name= 'login'),
    path('logout/',views. LogoutView.as_view()),
    path('user/',views.UserView.as_view()),
    # Producview Api
    path('list/',views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductDetailView.as_view()),
    # design Api
    path("update/<int:id>/",views.update_product,name = 'update'),
# can pass the query parmas ex:  http://127.0.0.1:8000/api/product-detail/?brand=madhur
    path('product-detail/',views.ProductDetailBrand.as_view(), name='snippet-detail'),
    
]
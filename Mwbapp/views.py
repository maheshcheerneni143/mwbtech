from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import RegisterSerializer,Add_ProductSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User,Add_Product
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from rest_framework import status
import jwt,datetime
from django.conf import settings
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


# Register
class RegisterView(APIView):
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Check if password and confirm password match
            if serializer.validated_data.get('password') == serializer.validated_data.get('confirm_password'):
                # Save only the password to the database
                user = serializer.save()
                user.set_password(serializer.validated_data.get('password'))
                user.save()
                return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Password and confirm password do not match'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# LOgin user
class LoginView(APIView):
    
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        user =User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("User not found")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response
        # return Response({'message':"successfully login"})
# Logout user
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

# SHOWS USERS
class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['user_id']).first()
        serializer = RegisterSerializer(user)
        return Response(serializer.data)


class ProductList(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload.get('user_id')
            print(user_id)
            products = Add_Product.objects.all()
            serializer = Add_ProductSerializer(products,many=True)
            return Response(serializer.data)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
    # Create Data
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload.get('user_id')
            serializer = Add_ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

class ProductDetailView(APIView):
    def get_object(self, pk):
        try:
            return Add_Product.objects.get(pk=pk)
        except Add_Product.DoesNotExist:
            raise Http404
    def get(self,request,pk,format=None):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload.get('user_id')
            # ===================
            snippet = self.get_object(pk)
            serializer = Add_ProductSerializer(snippet)

        # Extract the brand from the URL parameters
            brand = request.query_params.get('brand', None)

            if brand:
                products = Add_Product.objects.filter(brand=brand)
                product_serializer = Add_ProductSerializer(products, many=True)
                return Response(product_serializer.data)
            else:
                return Response(serializer.data)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
    def put(self,request,pk,format=None):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload.get('user_id')
            # ===================
            snippet = self.get_object(pk)
            serializer = Add_ProductSerializer(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # ===============================================
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
    def delete(self,request,pk,format=None):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload.get('user_id')
            # ===================
            snippet = self.get_object(pk)
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            # ===============================================
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

# Update design
# @login_required(login_url='login')
# @csrf_exempt
def update_product(request, id):
    # product = get_object_or_404(Add_Product, id=id)
    product = Add_Product.objects.get(id=id)
    if product:
        if request.method == 'POST':
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return HttpResponse("SUccessfully Updated",id)
            else:
                return HttpResponse("product Not found ",id)
        else:
            form = ProductForm(instance=product)
        return render(request, 'update_product.html', {'form': form, 'id': id})
    else:
        return HttpResponse("Not found")

# PRODUCTVIEW THROUGH BRAND
class ProductDetailBrand(APIView):
    serializer_class = Add_ProductSerializer
    def get(self,request,format=None):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload.get('user_id')
            print(user_id)
            queryset = self.get_queryset()
            brand = request.query_params.get('brand', None)
            if brand is not None:
                snippets = queryset.filter(brand=brand)
                serializer = Add_ProductSerializer(snippets, many=True)
                return Response(serializer.data)
            else:
                return Response({'message': 'No brand parameter provided'}, status=status.HTTP_400_BAD_REQUEST)
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
    def get_queryset(self):
        return Add_Product.objects.all()






    



    









from rest_framework import serializers
from .models import User
from .models import Add_Product

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=10, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'confirm_password', 'mobile_number']
        extra_kwargs= {
            'password': {'write_only': True},
        }
        
   

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        confirm_password = validated_data.pop('confirm_password', None)

        if password is not None and confirm_password is not None:
            if password != confirm_password:
                raise serializers.ValidationError("Passwords do not match.")

        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance



class Add_ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Add_Product
        fields = ['name', 'Category', 'brand', 'price', 'quantity', 'Description']
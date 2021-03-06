from rest_framework import serializers
from .models import User
from .models import Item
from .models import Order
from .models import Structure
from .models import Deliverer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class DeliveryBoySerializer(serializers.ModelSerializer):

    class Meta:
        model = Deliverer
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class MyOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('item_list', 'amount', 'status', 'delivery_type', 'order_time')


class StructureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Structure
        fields = '__all__'


class StructureCatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Structure
        fields = ('category_name', 'image')

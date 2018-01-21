from .serializers import UserSerializer
from .serializers import ItemSerializer
from .serializers import OrderSerializer
from .serializers import MyOrderSerializer
from .serializers import StructureSerializer
from .serializers import StructureCatSerializer
from .serializers import DeliveryBoySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User
from .models import Item
from .models import Order
from .models import Structure
from .models import Deliverer
import ast


class UserSignUp(APIView):

    def post(self, request):

            user_data = request.data
            user_phone = user_data['phone']
            check = User.objects.filter(phone=user_phone)
            serialized_data = UserSerializer(check, many=True)
            if serialized_data.data:
                return Response({'status': 'User already exists'})
            else:
                u = User()
                user_phone = user_data['phone']
                u.phone = user_phone
                user_name = user_data['name']
                u.name = user_name

                user_password = user_data['password']
                u.password = user_password

                user_address = user_data['address']
                u.address = user_address
                u.save()
                return Response({'status': 'success'})


class UserLogIn(APIView):

    def post(self, request):

        user_data = request.data
        user_phone = user_data['phone']
        user_password = user_data['password']

        try:
            check = User.objects.filter(phone=user_phone)
            serialized_data = UserSerializer(check, many=True)
            if user_password == serialized_data.data[0]['password']:
                return Response({'login': 'success', 'id': serialized_data.data[0]['id']})

            else:
                return Response({'login': 'wrong password'})

        except IOError:
            return Response({'login': 'User not registered'})


class DeliveryBoyLogIn(APIView):

    def post(self, request):

        user_data = request.data
        user_phone = user_data['phone']
        user_password = user_data['password']

        try:
            check = Deliverer.objects.filter(phone=user_phone)
            serialized_data = DeliveryBoySerializer(check, many=True)
            if user_password == serialized_data.data[0]['password']:
                return Response({'login': 'success', 'id': serialized_data.data[0]['id'],
                                 'name': serialized_data.data[0]['name']})

            else:
                return Response({'login': 'wrong password'})

        except IOError:
            return Response({'login': 'User not registered'})


class ViewCategories(APIView):

    def get(self, request):
        category_data = Structure.objects.all()
        serialized_data = StructureCatSerializer(category_data, many=True)
        return Response(serialized_data.data)


class ViewSubCategories(APIView):

    def post(self, request):

        data = request.data
        category = data['category']

        category_data = Structure.objects.filter(category_name=category)
        serialized_data = StructureSerializer(category_data, many=True)
        return Response({'sub_categories': serialized_data.data[0]['sub_category_name']})


class GetItem(APIView):

    def post(self, request):

        item_data = request.data
        item_sub_category = item_data['sub_category']
        page_no = item_data['page_no']
        try:
            response_data = Item.objects.filter(sub_category=item_sub_category)
            if not response_data:
                return Response({'status': 'no category found'})
            else:

                paginator = Paginator(response_data, 10)
                try:
                    serialized_data = ItemSerializer(paginator.page(page_no), many=True)
                except PageNotAnInteger:
                    serialized_data = ItemSerializer(paginator.page(1), many=True)
                    return Response(serialized_data.data)
                except EmptyPage:
                    return Response([{'status': 'no more data'}])

        except IOError:
            return Response({'status': 'no data'})

        else:
            return Response(serialized_data.data)


class ShowCart(APIView):

    def post(self, request):

        customer_data = request.data
        customer_id = customer_data['id']
        try:
            user_data = User.objects.filter(id=customer_id)
            serialized_data = UserSerializer(user_data, many=True)
            cart_data = serialized_data.data[0]['cart']

        except IOError:
            return Response({'status': 'no data'})

        else:
            return Response(cart_data)


class AddCart(APIView):

    def post(self, request):

        customer_data = request.data
        customer_id = customer_data['id']
        item_name = customer_data['item_name']
        item_amount = customer_data['item_amount']
        try:
            user_data = User.objects.filter(id=customer_id)
            serialized_data = UserSerializer(user_data, many=True)
            cart_data = serialized_data.data[0]['cart']
            new_cart = ast.literal_eval(cart_data)
            new_cart.update({item_name: item_amount})
            User.objects.filter(id=customer_id).update(cart=new_cart)

        except IOError:
            return Response({'status': 'failure'})

        else:
            return Response({'status': 'Added to your cart'})


class PlaceOrder(APIView):

    def post(self, request):
        customer_data = request.data
        customer_id = customer_data['id']
        payment_type = customer_data['payment_type']

        user_data = User.objects.filter(id=customer_id)
        serialized_data = UserSerializer(user_data, many=True)

        o = Order()
        o.customer_id = customer_id
        o.save()
        o.delivery_type = payment_type
        o.save()
        o.customer_name = serialized_data.data[0]['name']
        o.save()
        o.customer_address = serialized_data.data[0]['address']
        o.save()
        o.item_list = serialized_data.data[0]['cart']
        o.save()

        # amount calculations #
        bill = 0
        item_list = ast.literal_eval(serialized_data.data[0]['cart'])
        for item, amount in item_list.items():
            item_data_model = Item.objects.filter(name=item)
            item_serialized_data = ItemSerializer(item_data_model, many=True)
            item_price = item_serialized_data.data[0]['price']
            net_price = float(amount)*item_price
            bill = float(bill) + net_price

        o.amount = bill
        o.save()
        o.status = "placed"
        o.save()

        new_cart = ast.literal_eval(serialized_data.data[0]['cart'])
        new_cart.clear()
        User.objects.filter(id=customer_id).update(cart=new_cart)

        return Response({'status': 'success', 'bill': bill})


class ViewOrders(APIView):

    def get(self, request):
        orders = Order.objects.all().order_by('-id')
        serialized_data = OrderSerializer(orders, many=True)
        return Response(serialized_data.data)


class ViewPendingOrders(APIView):

    def get(self, request):
        orders = Order.objects.filter(status="placed").order_by('-id')
        serialized_data = OrderSerializer(orders, many=True)
        return Response(serialized_data.data)


class ViewDeliveredOrders(APIView):

    def get(self, request):
        orders = Order.objects.filter(status="Delivered").order_by('-id')
        serialized_data = OrderSerializer(orders, many=True)
        return Response(serialized_data.data)


class RemoveFromCart(APIView):

    def post(self, request):

        try:
            data = request.data
            item_name = data['item_name']
            customer_id = data['customer_id']

            user_data = User.objects.filter(id=customer_id)
            serialized_data = UserSerializer(user_data, many=True)
            cart_data = serialized_data.data[0]['cart']
            new_cart = ast.literal_eval(cart_data)
            del new_cart[item_name]
            User.objects.filter(id=customer_id).update(cart=new_cart)

            return Response({'status': 'success'})

        except IOError:
            return Response({'status': 'error'})


class MyDetails(APIView):

    def post(self, request):
        customer_data = request.data
        customer_id = customer_data['id']

        user_data = User.objects.filter(id=customer_id)
        serialized_data = UserSerializer(user_data, many=True)

        user_name = serialized_data.data[0]['name']
        user_phone = serialized_data.data[0]['phone']
        user_address = serialized_data.data[0]['address']

        return Response({'name': user_name, 'phone': user_phone, 'address': user_address})


class MyOrders(APIView):

    def post(self, request):
        customer_data = request.data
        customer_id = customer_data['id']

        user_orders = Order.objects.filter(customer_id=customer_id)
        serialized_data = MyOrderSerializer(user_orders, many=True)

        return Response(serialized_data.data)


class SearchItems(APIView):

    def post(self, request):
        search_data = request.data
        search_item = search_data['text'].lower()
        page_no = search_data['page_no']

        item_details = Item.objects.filter(name__contains=search_item)
        paginator = Paginator(item_details, 10)

        try:
            serialized_data = ItemSerializer(paginator.page(page_no), many=True)
            return Response(serialized_data.data)
        except PageNotAnInteger:
            serialized_data = ItemSerializer(paginator.page(1), many=True)
            return Response(serialized_data.data)
        except EmptyPage:
            # serialized_data = ItemSerializer(paginator.page(paginator.num_pages), many=True)
            # return Response(serialized_data.data)
            return Response([{'status': 'no more data'}])


class EditItemDetails(APIView):

    def post(self, request):
        item_data = request.data
        item_name = item_data['item_name']
        item_new_price = item_data['new_price']

        Item.objects.filter(name=item_name).update(price=item_new_price)

        return Response({'status': 'success'})


class Revenue(APIView):

    def get(self, request):
        order_data = Order.objects.all().order_by('-id')
        serialized_data = OrderSerializer(order_data, many=True)
        bill = 0
        for i in range(len(serialized_data.data)):
            amount = serialized_data.data[i]['amount']
            bill = amount + float(bill)

        return Response({'revenue': bill})


class ChangeStatus(APIView):

    def post(self, request):
        order_data = request.data
        order_id = order_data['order_id']

        Order.objects.filter(id=order_id).update(status='Delivered')

        return Response({'status': 'success'})


class ForwardOrder(APIView):

    def post(self, request):
        order_id = request.data['order_id']
        delivery_boy_id = request.data['boy_id']

        Order.objects.filter(id=order_id).update(delivery_boy=delivery_boy_id)
        Order.objects.filter(id=order_id).update(status="progress")

        return Response({'status': 'success'})


class DeliveryBoyOrders(APIView):

    def post(self, request):
        delivery_boy_id = request.data['boy_id']
        orders = Order.objects.filter(delivery_boy=delivery_boy_id)

        serialized_data = OrderSerializer(orders, many=True)
        return Response(serialized_data.data)


class DeliveryBoyDetails(APIView):

    def get(self, request):
        delivery_boys = Deliverer.objects.all().order_by('-id')
        serialized_data = DeliveryBoySerializer(delivery_boys, many=True)
        return Response(serialized_data.data)

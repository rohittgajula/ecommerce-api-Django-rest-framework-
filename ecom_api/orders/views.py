from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination

from .models import Order, OrderItem
from product.models import Product
from .serializers import OrderSerializers
from .filters import OrderFilter

from drf_yasg.utils import swagger_auto_schema


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_orders(request):
  filterset = OrderFilter(request.GET, queryset=Order.objects.all().order_by('id'))
  # for total count
  count = filterset.qs.count()
  # pagination
  resPerPage = 3
  paginator = PageNumberPagination()
  paginator.page_size = resPerPage

  queryset = paginator.paginate_queryset(filterset.qs, request)
  serializer = OrderSerializers(queryset, many=True)
  return Response({
    'count':count,
    'resPerPage':resPerPage,
    'orders':serializer.data
  }, status.HTTP_200_OK)

@api_view(['GET'])
def get_order(request, pk):
  order = get_object_or_404(Order, id=pk)
  serializer = OrderSerializers(order, many=False)
  return Response({
    'order':serializer.data
  }, status.HTTP_200_OK)


@swagger_auto_schema(method='POST', request_body=OrderSerializers)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):
  user = request.user
  data = request.data

  order_items = data['orderItems']
  if order_items and len(order_items) == 0:
    return Response({
      'error':'You need to add atleast one product.'
    }, status.HTTP_404_NOT_FOUND)
  else:
    
    total_amount = sum(item['price'] * item['quantity'] for item in order_items)

    order = Order(user=user, total_amount=total_amount)
    for attr, value in data.items():
      setattr(order, attr, value)
    order.save()

    for i in order_items:
      product = Product.objects.get(id=i['product'])
      item = OrderItem.objects.create(
        product = product,
        order = order,
        name = product.name,
        quantity = i['quantity'],
        price = i['price']
      )

      product.stock -= item.quantity
      product.save()

    serializer = OrderSerializers(order, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, pk):
  order = get_object_or_404(Order, id=pk)
  order.delete()
  return Response({
    'details':'Order deleted sucessfully.'
  }, status.HTTP_200_OK)


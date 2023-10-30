from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, TableProductsSerializer
from .models import Product, Image, Variant
from .serializers import ProductWriteSerializer
from datetime import datetime
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


@api_view(['GET'])
def productApiOverview(request):
    api_urls = {
        'Product List': 'product-list/',
        'Product Detail View': 'product-details/<int:id>/',
        'Create Product': 'create-product/',
        'Update Product': 'update-product/<int:id>/',
        'Delete Product': 'delete-product/<int:id>/',

        'Get Products for table with pagination': 'table/',
        'Filter Products as product_type with pagination': 'products/by_type/<str:product_type>/',
        'Filter Products as multiple/single tags': 'products/by-tags/?tags=tag1,tag2',
    }
    return Response(api_urls)


"""Api for table module: Get Products for table with pagination"""
@api_view(['GET'])
def get_table_products(request):
    products = Product.objects.all()
    paginator = PageNumberPagination()
    paginator.page_size = 6
    paginated_products = paginator.paginate_queryset(products, request)

    serializer = TableProductsSerializer(paginated_products, many=True)
    return paginator.get_paginated_response(serializer.data)


"""Filter module: Filter Products as product_type with pagination"""
@api_view(['GET'])
def filter_product_by_type(request, product_type):
    products = Product.objects.filter(product_type=product_type)
    paginator = PageNumberPagination()
    paginator.page_size = 4
    paginated_products = paginator.paginate_queryset(products, request)

    serializer = TableProductsSerializer(paginated_products, many=True)
    return paginator.get_paginated_response(serializer.data)


"""Filter module: Filter Products By multiple Tags"""
@api_view(['GET'])
def filter_products_by_tags(request):
    tags = request.GET.get('tags', '').split(',')
    # print(tags)

    products = Product.objects.filter(tags__icontains=tags[0].strip())
    # query = Q()
    # for tag in tags:
    #     query |= Q(tags__contains=tag.strip())
    for tag in tags[1:]:
        products = products | Product.objects.filter(tags__icontains=tag.strip())

    paginator = PageNumberPagination()
    paginator.page_size = 4
    paginated_products = paginator.paginate_queryset(products, request)

    serializer = TableProductsSerializer(paginated_products, many=True)
    response = paginator.get_paginated_response(serializer.data)
    return Response(response.data)


"""Get all available products details on single page"""
@api_view(['GET'])
def showAll(request):
    try:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""Get particular product details"""

@api_view(['GET'])
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""Add new Product to Database"""
@api_view(['POST'])
def create_product(request):
    product_data = request.data
    product_data['created_at'] = datetime.now()
    product_data['updated_at'] = datetime.now()
    image_data = product_data.pop('images', [])
    variants_data = product_data.pop('variants', [])
    try:
        serializer = ProductWriteSerializer(data=product_data)

        if serializer.is_valid():
            product = serializer.save()
            images = []
            for image_info in image_data:
                image_info['created_at'] = datetime.now()
                image_info['updated_at'] = datetime.now()
                image_info['product'] = product
                image = Image.objects.create(**image_info)
                images.append(image)
            variants = []
            for variant_info in variants_data:
                variant_info['created_at'] = datetime.now()
                variant_info['updated_at'] = datetime.now()
                variant_info['product'] = product
                variant = Variant.objects.create(**variant_info)
                variants.append(variant)

            product.images.set(images)
            product.variants.set(variants)
            product_serializer = ProductSerializer(product)
            return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""Update the existing product"""
@api_view(['PUT', 'PATCH'])
def update_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductWriteSerializer(product, data=request.data)
    elif request.method == 'PATCH':
        serializer = ProductWriteSerializer(product, data=request.data, partial=True)
    else:
        return Response({'error': 'Invalid method'}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        product.updated_at = datetime.now()
        product.save()
        serializer.save()

        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""Delete product"""
@api_view(['DELETE'])
def delete_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

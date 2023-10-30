from rest_framework import serializers

from .models import Product, Image, Variant


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    variants = VariantSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('id', 'created_at', 'updated_at')


class TableProductsSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id','product_image', 'product_type', 'tags', 'published_at']

    def get_product_image(self, product):
        first_image = product.images.filter(position=1).first()
        if first_image:
            return first_image.src
        return None
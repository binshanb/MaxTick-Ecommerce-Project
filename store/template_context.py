from .models import Product
from django.db.models import Min,Max

def get_filters(request):
    cats=Product.objects.distinct.values('category__name','category__id')
    # brands=Product.objects.distinct.values('brand__name','brand__id')
    minMaxPrice=Product.objects.aggregate(Min('price'),Max('price'))

    data={
        'cats':cats,
        # 'brands':brands,
        'minMaxPrice':minMaxPrice,
    }
    return data
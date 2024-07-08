# yourapp/filters.py
import django_filters
from django.db.models import F, ExpressionWrapper, DecimalField, Case, When, Value
from product.models import ProductVersion, Brand

class ProductVersionFilter(django_filters.FilterSet):
    is_new = django_filters.BooleanFilter(field_name='is_new')
    discount = django_filters.BooleanFilter(field_name='discount', method='filter_profitable')
    top_sales = django_filters.BooleanFilter(method='filter_top_sales')
    # min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    # max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_price = django_filters.NumberFilter(method='filter_min_price')
    max_price = django_filters.NumberFilter(method='filter_max_price')
    page = django_filters.NumberFilter(method='filter_page')
    page_size = django_filters.NumberFilter(method='filter_page_size')
    brand_id = django_filters.ModelChoiceFilter(queryset=Brand.objects.all())
    category_id = django_filters.NumberFilter(method='filter_by_category')

    class Meta:
        model = ProductVersion
        fields = ['is_new', 'discount', 'top_sales', 'min_price', 'max_price', 'page', 'page_size', 'brand_id', 'category_id'] 

    def filter_profitable(self, queryset, name, value):
        if value is True:
            # Check for non-null discounts
            return queryset.filter(discount__isnull=False)
        else:
            return queryset.filter(discount__isnull=True)
        return queryset
    
    def filter_top_sales(self, queryset, name, value):
        if value is True:
            # Filter products with sales > 0 and order by sales in descending order
            return queryset.filter(sales__gt=0).order_by('-sales')
        return queryset
    
    def filter_min_price(self, queryset, name, value):
        discounted_price = ExpressionWrapper(
            Case(
                When(discount__discount_type='percent', then=F('price') - (F('price') * F('discount__value') / 100)),
                When(discount__discount_type='amount', then=F('price') - F('discount__value')),
                default=F('price'),
                output_field=DecimalField()
            ),
            output_field=DecimalField()
        )
        return queryset.annotate(discounted_price=discounted_price).filter(discounted_price__gte=value)

    def filter_max_price(self, queryset, name, value):
        discounted_price = ExpressionWrapper(
            Case(
                When(discount__discount_type='percent', then=F('price') - (F('price') * F('discount__value') / 100)),
                When(discount__discount_type='amount', then=F('price') - F('discount__value')),
                default=F('price'),
                output_field=DecimalField()
            ),
            output_field=DecimalField()
        )
        return queryset.annotate(discounted_price=discounted_price).filter(discounted_price__lte=value)
    
    def filter_by_category(self, queryset, name, value):
        return queryset.filter(subcategory__category_id=value)

    def filter_page(self, queryset, name, value):
        if value is not None:
            self._page = value
        return queryset

    def filter_page_size(self, queryset, name, value):
        if value is not None:
            self._page_size = value
        return queryset

    def paginate_queryset(self, queryset):
        page = getattr(self, '_page', 1)
        page_size = getattr(self, '_page_size', 10)
        start = (page - 1) * page_size
        end = start + page_size
        return queryset[start:end]
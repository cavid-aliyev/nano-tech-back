# yourapp/filters.py
import django_filters
from django.db.models import F,Q, ExpressionWrapper, DecimalField, Case, When, Value, BooleanField, Count
from product.models import ProductVersion, Brand
from django.db.models.functions import Coalesce

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
    daily_special_discount = django_filters.BooleanFilter(method='filter_special_discount')
    ordering = django_filters.OrderingFilter(
        fields=(
            ('price', 'price'),
        ),
        field_labels={
            'price': 'Price',
        },
        label='Order by'
    )


    class Meta:
        model = ProductVersion
        fields = ['is_new', 'discount','daily_special_discount', 'top_sales', 'min_price', 'max_price', 'page', 'page_size', 'brand_id', 'category_id'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['ordering'].extra['choices'] = (
            ('price', 'Ascending Price'),
            ('-price', 'Descending Price'),
        )


    def filter_special_discount(self, queryset, name, value):
        if value:
            latest_special_discount = queryset.filter(special_discounts__is_active=True).order_by('-special_discounts__created_at').first()
            if latest_special_discount:
                return queryset.filter(id=latest_special_discount.id)
        return queryset


    def filter_profitable(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(discount__isnull=False) |
                Q(special_discounts__is_active=True)
            ).distinct()
        else:
            return queryset.filter(
                Q(discount__isnull=True) &
                Q(special_discounts__is_active=False)
            ).distinct()


    def filter_top_sales(self, queryset, name, value):
        if value is True:
            # Filter products with sales > 0 and order by sales in descending order
            return queryset.filter(sales__gt=0).order_by('-sales')
        return queryset


    def get_discounted_price_annotation(self):
        return ExpressionWrapper(
            Case(
                When(
                    special_discounts__is_active=True,
                    then=Case(
                        When(special_discounts__discount_type='percent', 
                             then=F('price') - (F('price') * F('special_discounts__value') / 100)),
                        When(special_discounts__discount_type='amount', 
                             then=F('price') - F('special_discounts__value')),
                        default=F('price'),
                        output_field=DecimalField()
                    )
                ),
                default=Case(
                    When(discount__discount_type='percent', 
                         then=F('price') - (F('price') * F('discount__value') / 100)),
                    When(discount__discount_type='amount', 
                         then=F('price') - F('discount__value')),
                    default=F('price'),
                    output_field=DecimalField()
                ),
                output_field=DecimalField()
            ),
            output_field=DecimalField()
        )

    def filter_max_price(self, queryset, name, value):
        discounted_price = self.get_discounted_price_annotation()
        return queryset.annotate(discounted_price=discounted_price).filter(discounted_price__lte=value).distinct()

    def filter_min_price(self, queryset, name, value):
        discounted_price = self.get_discounted_price_annotation()
        return queryset.annotate(discounted_price=discounted_price).filter(discounted_price__gte=value).distinct()

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
    
    # def filter_queryset(self, queryset):
    #     queryset = super().filter_queryset(queryset)
    #     ordering_value = self.form.cleaned_data.get('ordering')
    #     if ordering_value:
    #         queryset = queryset.order_by(ordering_value)
    #     return queryset
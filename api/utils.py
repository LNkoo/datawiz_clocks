from django.db.models import Min, Max


def get_available_filters(qs):
    available_filters = [
        {
            "name": "price",
            "type": "diapason",
            "values": [qs.aggregate(Min("price"))['price__min'],
                       qs.aggregate(Max("price"))['price__max']]
        },
        {
            "name": "brand",
            "type": "choices",
            "values": [item['characteristic__brand'] for item in(
                qs
                .values("characteristic__brand")
                .distinct()
            )]

        },
        {
            "name": "country",
            "type": "choices",
            "values": [item ['characteristic__country'] for item in(
                qs
                .values("characteristic__country")
                .distinct()
            )]
        }
    ]
    return available_filters


def filter_by_price(qs, price_diapason):
    price_diapason.sort()
    return qs.filter(
        price__gte=price_diapason[0], price__lte=price_diapason[1]
    )


def filter_by_brand(qs, brand_names):
    return qs.filter(characteristic__brand__in=brand_names)


def filter_by_country(qs, country_names):
    return qs.filter(characteristic__country__in=country_names)

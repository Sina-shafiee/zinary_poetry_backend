import json
import re
import math
from django.db.models import Q


def apply_query_filters(
    queryset, page=1, per_page=10, search=None, search_fields=None, sort=None
):
    if search and search_fields:
        search_query = Q()
        for field in search_fields:
            search_query |= Q(**{f"{field}__icontains": search})
        queryset = queryset.filter(search_query)

    if sort:
        order_by_args = []
        sort_list = json.loads(sort)
        for sort_item in sort_list:
            field = re.sub(r"([a-z])([A-Z])", r"\1_\2", sort_item.get("id")).lower()
            desc = sort_item.get("desc", False)
            if field:
                if desc:
                    order_by_args.append(f"-{field}")
                else:
                    order_by_args.append(field)
        if order_by_args:
            queryset = queryset.order_by(*order_by_args)

    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 10

    total_items = queryset.count()
    total_pages = math.ceil(total_items / per_page)

    start = (page - 1) * per_page
    end = start + per_page
    paginated_queryset = queryset[start:end]

    return {
        "queryset": paginated_queryset,
        "total_pages": total_pages,
        "current_page": page,
        "total_items": total_items,
    }

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.db.models import Func, Value, CharField, F
from django.db.models.query_utils import Q

from goods.models import Product

class Left(Func):
    function = 'LEFT'
    output_field = CharField()

def q_search(query):
    if query.isdigit() and len(query) <= 6:
        return Product.objects.filter(id=int(query))

    vector = SearchVector("name", "description")
    search_query = SearchQuery(query)

    results = Product.objects.annotate(
        short_name=Left(F("name"), Value(25)),
        short_description=Left(F("description"), Value(50)),
        rank=SearchRank(vector, search_query)
    ).filter(rank__gt=0).order_by("-rank")

    results = results.annotate(
        headline=SearchHeadline(
            "short_name",
            search_query,
            start_sel='<span style="background-color: yellow">',
            stop_sel="</span>"
        ),
    )

    results = results.annotate(
        bodyline=SearchHeadline(
            "short_description",
            search_query,
            start_sel='<span style="background-color: yellow">',
            stop_sel="</span>"
        ),
    )

    if not results.exists():
        keywords = [word for word in query.split() if len(word) > 2]
        q_objects = Q()

        for token in keywords:
            q_objects |= Q(name__icontains=token)
            q_objects |= Q(description__icontains=token)

        results = Product.objects.filter(q_objects)

    return results
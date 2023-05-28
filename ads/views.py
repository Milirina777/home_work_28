import json
import math

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category, ADS
from dj_project import settings


def root(request):
    return JsonResponse({
        "status": "ok"
    })

@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('name')

        response = []
        for category in self.object_list.all():
            response.append({
                "id": category.id,
                "name": category.name,
            })

        return JsonResponse(response, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        cat_data = json.loads(request.body)
        category = Category.objects.create(name=cat_data["name"])

        category.save()

        return JsonResponse({
                "name": category.name
                            })


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsListView(ListView):
    model = ADS
    queryset = ADS.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('-price')

        total_ad = self.object_list.count()
        page = int(request.GET.get("page", 0))
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_obj = paginator.get_page(page)

        response = []
        response.append({
            "totals": total_ad,
            "num_page": math.ceil(total_ad / settings.TOTAL_ON_PAGE)
        })


        for ad in page_obj:
            category = Category.objects.filter(id=ad.category_id_id)
            category_name = category[0].name
            response.append({
                "id": ad.id,
                "name": ad.name,
                "description": ad.description,
                "author": ad.author_id_id,
                "price": ad.price,
                "is_published": ad.is_published,
                "category": category_name,
            })


        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdsCreateView(CreateView):
    model = ADS
    fields = ["name", "author_id", "price", "description", "is_published"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)
        ad = ADS.objects.create(
            name=ad_data["name"],
            author_id_id=ad_data["author_id"],
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            category_id_id=ad_data["category_id"],
        )

        ad.save()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author_id_id,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsUpdateView(UpdateView):
    model = ADS
    fields = ["name", "author_id", "price", "description", "is_published"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)
        self.object.name=ad_data["name"]
        self.object.price=ad_data["price"]
        self.object.description=ad_data["description"]

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author_id_id,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsDeleteView(DeleteView):
    model = ADS
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class AdsDetailView(DetailView):
    model = ADS

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author_id_id,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdImageUpload(UpdateView):
    model = ADS
    fields = ["name", "author_id", "price", "description", "is_published"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image")
        self.object.save()

        return JsonResponse({"name": self.object.name, "image": self.object.image.url})

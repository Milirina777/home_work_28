import json
import math

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from ads.models import User, Location, ADS
from dj_project import settings


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    model = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.annotate(t_ads=Count('ads', filter=Q(ads__is_published=True)))


        total_ad = self.object_list.count()
        page = int(request.GET.get("page", 0))
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_obj = paginator.get_page(page)

        response = []
        response.append({
            "totals": total_ad,
            "num_page": math.ceil(total_ad / settings.TOTAL_ON_PAGE)
        })
        for user in page_obj:
            location = Location.objects.filter(id=user.location_id_id)[0].name

            response.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "role": user.role,
                "password": user.password,
                "age": user.age,
                "location": location,
                "total_ads": user.t_ads

            })

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ["first_name", "last_name", "username"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)
        user = User.objects.create(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            username=user_data["username"],
            password=user_data["password"],
            role=user_data["role"],
            age=user_data["age"],
            location_id_id=user_data["location_id"],
        )

        user.save()

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "password": user.password,
            "age": user.age,
            "location_id": user.location_id_id,
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ["first_name", "last_name", "username"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)
        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data["last_name"]
        self.object.username = user_data["username"]
        self.object.password = user_data["password"]
        self.object.role = user_data["role"]
        self.object.age = user_data["age"]
        self.object.location_id_id = user_data["location_id"]

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "password": self.object.password,
            "age": self.object.age,
            "location_id": self.object.location_id_id,
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)

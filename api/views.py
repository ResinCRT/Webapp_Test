from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
from api.models import OpenBookmark

class BaseApiView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
class BookmarkApi(BaseApiView):
    def get(self, request, id=None):
        if id : # 단일 항목 요청
            bookmark = OpenBookmark.objects.get(id=id)
            data = model_to_dict(bookmark)
            return JsonResponse(data)
        else : # 목록 요청
            datas = list(map(model_to_dict, OpenBookmark.objects.all()))
            return JsonResponse({"datas" : datas})
    def post(self, request):
        json_data = json.loads(request.body.decode("utf-8"))
        print(json_data)
        bookmark = OpenBookmark(**json_data)
        bookmark.save()
        data = model_to_dict(bookmark)
        return JsonResponse(data)
    def put(self, request, id):
        bookmark = OpenBookmark.objects.get(id=id)
        json_data = json.loads(request.body.decode("utf-8"))
        bookmark.title = json_data["title"]
        bookmark.url = json_data["url"]
        bookmark.save()
        data = model_to_dict(bookmark)
        return JsonResponse(data)
    def delete(self, request, id):
        bookmark = OpenBookmark.objects.get(id=id)
        bookmark.delete()
        return JsonResponse({"result": "OK"})
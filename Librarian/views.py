import os
import requests
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import *

from Librarian.models.automaton import Automaton
from Librarian.utils.utils import KMP, map_library

try:
    from Librarian import env
except:
    LIBRARY = os.path.dirname(os.path.dirname(
        __file__)) + os.path.sep + "static" + os.path.sep + "library"


class BasicSearch(APIView):
    def get(self, request, format=None):
        keyword = request.GET.get('keyword')
        if keyword is None:
            return HttpResponseBadRequest("Keyword has not been defined")
        return HttpResponse(map_library(keyword, KMP))


class AdvancedSearch(APIView):
    def get(self, request, format=None):
        pattern = request.GET.get('pattern')
        if pattern is None:
            return HttpResponseBadRequest("Pattern has not been defined")
        return HttpResponse(map_library(pattern, lambda pattern, text: Automaton.dfa(pattern).walk(text)))


class GetBook(APIView):
    def get(self, request, format=None):
        book_id = request.GET.get("id")
        try:
            file_name = book_id + ".txt"
            with open(os.path.join(env.LIBRARY, file_name), 'r', errors="ignore") as f:
                response = HttpResponse(f.read())
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response
        except Exception:
            return HttpResponseNotFound()

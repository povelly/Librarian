import os
import requests
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import HttpResponseBadRequest

from Librarian.models.automaton import Automaton
from Librarian.utils.utils import KMP, map_library


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


class Test(APIView):
    def get(self, request, format=None):
        return HttpResponse("For testing purpose")

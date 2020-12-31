import os, requests, json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from Librarian.utils.kmp import KMP
from Librarian import env

class BasicSearch(APIView):
    def get(self, request, format=None):
        keyword = request.GET.get('keyword')
        if keyword is None:
            return HttpResponseBadRequest("Keyword has not been defined")
        return HttpResponse(mapLibrary(keyword, KMP))

class AdvancedSearch(APIView):
    def get(self, request, format=None):
        return HttpResponse("La page de la recherche advanced")

class Test(APIView):
    def get(self, request, format=None):
        return HttpResponse("x")

def mapLibrary(pattern, criterion):
    matches = []
    for fileName in os.listdir(env.LIBRARY):
        with open(os.path.join(env.LIBRARY, fileName), 'r') as f:
            if criterion(pattern, f.read()):
                matches.append(fileName)
    return json.dumps(matches)

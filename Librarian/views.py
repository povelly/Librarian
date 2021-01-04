import os, requests, json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from Librarian.utils.kmp import KMP
import Librarian.regex
from Librarian.regex.automaton import Automaton
from Librarian import env
from Librarian.regex.regex import RegEx

class BasicSearch(APIView):
    def get(self, request, format=None):
        keyword = request.GET.get('keyword')
        if keyword is None:
            return HttpResponseBadRequest("Keyword has not been defined")
        return HttpResponse(mapLibrary(keyword, KMP))

class AdvancedSearch(APIView):
    def get(self, request, format=None):
        pattern = request.GET.get('pattern')
        if pattern is None:
            return HttpResponseBadRequest("Pattern has not been defined")
        def criterion(pattern, text):
            return Automaton.dfa(pattern).walk(text)
        return HttpResponse(mapLibrary(pattern, criterion))

        # return HttpResponse(mapLibrary(keyword, KMP))

class Test(APIView):
    def get(self, request, format=None):
        return HttpResponse("x")

def mapLibrary(pattern, criterion):
    matches = []
    for fileName in os.listdir(env.LIBRARY):
        with open(os.path.join(env.LIBRARY, fileName), 'r') as f:
            occurences = criterion(pattern, f.read())
            if occurences > 0:
                matches.append({"file": fileName, "occurences": occurences})
    return json.dumps(matches)

from django.shortcuts import render

from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
import coreapi
from bs4 import BeautifulSoup

# Create your views here.

@api_view(['GET'])
def videos_list(request, lang):
    client = coreapi.Client()
    schema = client.get('https://www.ted.com/talks?sort=popular&language=sq')
    soup = BeautifulSoup(schema, "html.parser")
    pages = soup.find_all("a", class_="pagination__item")[-1].get_text()
    return JsonResponse({'message': 'There are {} pages of videos for the language {}'.format(pages, lang)}, status=status.HTTP_200_OK)
    
from django.shortcuts import render

import os
import boto3

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view


# Create your views here.
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_BUCKET_NAME = os.environ['TED_ASSETS_BUCKET_NAME']


session = boto3.Session(
   aws_access_key_id=AWS_ACCESS_KEY_ID,
   aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

@api_view(['POST'])
def upload_file_to_s3(request):
    """
    Uploads a file to AWS S3. Usage:
    >>> upload_file_to_s3('/tmp/business_plan.pdf')
    """
    if request.method == 'POST':
        assets_dir = "assets/"
        if assets_dir is None:
            raise ValueError("Assets directory does not exist")

        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        s3 = session.resource('s3')

        for file_name in os.listdir(assets_dir):
            data = open(os.path.normpath(assets_dir + file_name), 'rb')
            s3.Bucket(AWS_BUCKET_NAME).put_object(Key=file_name, Body=data)
        return JsonResponse({"message": "Data are uploaded"}, status=status.HTTP_200_OK)
import boto3
import json


from uuid import uuid4


from django.http   import JsonResponse, HttpResponse
from django.views  import View

from my_settings     import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY
from lectures.models import Lecture, LectureImage

class FileView(View):
    s3_client = boto3.client(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )
    
    def post(self, request):
        try:

            file = request.FILES.getlist['filename']
            BUCKET_ADDRESS = 'https://woosbucket.s3.ap-northeast-2.amazonaws.com'
            BUCKET_DIRECTORY = 'image'
            
            url =f"{BUCKET_DIRECTORY}/{str(uuid4())}"
            urls =f"{BUCKET_ADDRESS}/{url}"
            self.s3_client.upload_fileobj(
                file, 
                "woosbucket",
                url,
                ExtraArgs={
                    "ContentType": file.content_type
                }
            )
            
            
            #lecture, is_created = 
            Lecture.objects.create(
                name                = request.POST['name'],
                price               = request.POST['price'],
                discount_rate       = request.POST['discount_rate'],
                thumbnail_image_url = urls,
                description         = request.POST['description'],
                user_id             = request.POST['user_id'],
                difficulty_id       = request.POST['difficulty_id'],
                subcategory_id      = request.POST['subcategory_id']
            )
            # if is_created:
                
            #     self.s3_client.upload_fileobj(
            #     image, 
            #     "woosbucket",
            #     url,
                
            #     ExtraArgs={
            #         "ContentType": file.content_type
            #     }
            # )
                
                
            #     LectureImage.objects.create(
            #         title      = request.POST['title'],
            #         image_url  = urls,
            #         sequence   = request.POST['sequence'],
            #         lecture_id = lecture.id
                    
            #     )
            return JsonResponse({"message" : "success"},status=201)        
        
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"},status=400)
        
        
        # file   = request.FILES['filename']
        # data = request.POST
        # # print(data)
       
        # BUCKET_ADDRESS = 'https://woosbucket.s3.ap-northeast-2.amazonaws.com'
        # BUCKET_DIRECTORY = 'image'
        # self.s3_client.upload_fileobj(
        #     file, 
        #     "woosbucket",
        #     f"{BUCKET_DIRECTORY}/{uuid4()}",
        #     ExtraArgs={
        #         "ContentType": file.content_type
        #     }
        # ) 

        # return HttpResponse(status= 200)
        
              

        """
        목적: 수업을 등록
        
        1. 수업에 대한 정보를 디비에 저장
        2. 이미지 저장(어떤 수업의 이미지인지 알아야됨) 저 주소를 조합해서 db에 저장하면 됩니다.
        
        
        """
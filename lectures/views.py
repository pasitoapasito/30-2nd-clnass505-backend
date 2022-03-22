from asyncio import trsock
import boto3

from uuid          import uuid4
from django.http   import JsonResponse
from django.views  import View
from django.db     import transaction,IntegrityError

from users.models    import User
from lectures.models import Lecture, LectureImage
from core.decorator  import signin_decorator
from my_settings     import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,BUCKET_ADDRESS,BUCKET_DIR_THUMNAIL,BUCKET_DIR_IMAGE,BUCKET_DIR_PROFILE 
from core.storage import s3_client, FileUpload, google_client

class LecturesView(View):    
    @signin_decorator
    def post(self, request):
        try:
            thumnail       = request.FILES['thumnail']
            lecture_images = request.FILES.getlist('lecture_images')
            profile        = request.FILES['profile']
            
            user           = request.user
            user.nickname          = request.POST['nickname']
            user.description       = request.POST['introduce']
            
            name          = request.POST['name']
            price         = request.POST['price']
            discount_rate = request.POST['discount_rate']
            
            description    = request.POST['description']
            difficulty_id  = request.POST['difficulty_id']
            subcategory_id = request.POST['subcategory_id']
            title          = request.POST['title']

            file_handler = FileUpload(google_client)

            with transaction.atomic():
                thumnail_url        = f"{BUCKET_DIR_THUMNAIL}/{str(uuid4())}"
                profile_image_url   = f"{BUCKET_DIR_PROFILE}/{str(uuid4())}"
                
                file_handler.upload(profile)
            
                user.profile_image_url = f"{BUCKET_ADDRESS}/{profile_image_url}"
                user.save()
              
                file_handler.upload(thumnail)
                
                lecture = Lecture.objects.create(
                        name                = name,
                        price               = price,
                        discount_rate       = discount_rate,
                        thumbnail_image_url = f"{BUCKET_ADDRESS}/{thumnail_url}",
                        description         = description,
                        user_id             = user.id,
                        difficulty_id       = difficulty_id,
                        subcategory_id      = subcategory_id
                )
                
                lecture_images = []

                for idx, lecture_image in enumerate(lecture_images):
                    image_url  = f"{BUCKET_DIR_IMAGE}/{str(uuid4())}"
                    
                    file_handler.upload(lecture_image)
                
                    lecture_images.append(LectureImage(
                        title      = title,
                        image_url  = f"{BUCKET_ADDRESS}/{image_url}",
                        sequence   = idx + 1,
                        lecture_id = lecture.id
                    ))

                LectureImage.objects.bulk_create(lecture_images)       
                 
            return JsonResponse({"message" : "success"},status=201)        
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"},status=400)
        except transaction.TransactionManagementError:
            return JsonResponse({'message':'TransactionManagementError'}, status=400)
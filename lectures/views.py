import boto3

from uuid          import uuid4
from django.http   import JsonResponse
from django.views  import View

from users.models    import User
from lectures.models import Lecture, LectureImage
from core.decorator  import signin_decorator
from my_settings     import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY

class FileView(View):
    s3_client = boto3.client(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )
    @signin_decorator
    def post(self, request):
        try:
            profile  = request.FILES['profile']
            user     = request.user
           
            users    = User.objects.filter(id=user.id)
            user_ids = User.objects.get(id=user.id)
            BUCKET_ADDRESS    = 'https://woosbucket.s3.ap-northeast-2.amazonaws.com'
            BUCKET_DIRECTORY  = 'thumnail'
            BUCKET_DIRECTORY2 = 'image'
            BUCKET_DIRECTORY3 = 'profile'
            url          = f"{BUCKET_DIRECTORY}/{str(uuid4())}"
            urls         = f"{BUCKET_ADDRESS}/{url}"
            profile_url  = f"{BUCKET_DIRECTORY3}/{str(uuid4())}"
            profile_urls = f"{BUCKET_ADDRESS}/{profile_url}"
            
            self.s3_client.upload_fileobj(
                profile, 
                "woosbucket",
                profile_url,
                ExtraArgs={
                    "ContentType" : profile.content_type
                }
            )
           
            users.update(
                profile_image_url = profile_urls,
                nickname          = request.POST['nickname'],
                description       = request.POST['introduce']
            )
            
            file    = request.FILES['thumnail']
            files   = request.FILES.getlist('image')
    
            self.s3_client.upload_fileobj(
                file, 
                "woosbucket",
                url,
                ExtraArgs={
                    "ContentType": file.content_type
                }
            )
            
            lecture = Lecture.objects.create(
                    name                = request.POST['name'],
                    price               = request.POST['price'],
                    discount_rate       = request.POST['discount_rate'],
                    thumbnail_image_url = urls,
                    description         = request.POST['description'],
                    user_id             = user.id,
                    difficulty_id       = request.POST['difficulty_id'],
                    subcategory_id      = request.POST['subcategory_id']
            )
            
            for i in range(3):
                image_url  = f"{BUCKET_DIRECTORY2}/{str(uuid4())}"
                image_urls = f"{BUCKET_ADDRESS}/{image_url}"
                
                self.s3_client.upload_fileobj(
                    files[i], 
                    "woosbucket",
                    image_url,
                    ExtraArgs={
                        "ContentType": file.content_type
                    }
                )
            
                LectureImage.objects.create(
                        title      = request.POST['title'],
                        image_url  = image_urls,
                        sequence   = i,
                        lecture_id = lecture.id
                        
                    )
            return JsonResponse({"message" : "success"},status=201)        
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"},status=400)
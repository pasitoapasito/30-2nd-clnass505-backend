import boto3

from uuid             import uuid4
from django.views     import View
from django.http      import JsonResponse
from django.db        import transaction
from django.db.models import Avg

from lectures.models import Lecture, LectureImage
from users.models    import UserLecture, Like
from core.decorator  import public_decorator, signin_decorator
from core.storage    import FileUpload, s3_client
from my_settings     import (
    BUCKET_DIR_THUMBNAIL,
    BUCKET_DIR_IMAGE,
    BUCKET_DIR_PROFILE 
)

class LectureDetailView(View):
    @public_decorator
    def get(self, request, lecture_id):
        try:
            user    = request.user
            lecture = Lecture.objects\
                             .select_related('user', 'subcategory')\
                             .prefetch_related('lectureimage_set', 'review_set', 'like_set')\
                             .get(id=lecture_id)
                
            if UserLecture.objects.filter(user=user, lecture=lecture).exists():
                user_status = 'student'
                
            if not UserLecture.objects.filter(user=user, lecture=lecture).exists():
                user_status = 'potential_student'
                
            if lecture.user == user:
                user_status = 'creator'
            
            if user is None:
                user_status = None
            
            result = {
                'id'                        : lecture.id,
                'subcategory'               : lecture.subcategory.name,
                'creator_nickname'          : lecture.user.nickname,
                'creator_profile_image_url' : lecture.user.profile_image_url,
                'title'                     : lecture.name,
                'price'                     : lecture.price,
                'discount_rate'             : lecture.discount_rate if lecture.discount_rate else None,
                'discount_price'            : float(lecture.price) * (1-(lecture.discount_rate/100))\
                                              if lecture.discount_rate else None,
                'description'               : lecture.description,
                'difficulty'                : lecture.difficulty.name,
                'review_avg_rating'         : round(lecture.review_set.all().aggregate(Avg('rating'))['rating__avg'], 1)\
                                              if lecture.review_set.all() else None,
                'likes'                     : lecture.like_set.count(),
                'thumbnail_image_url'       : lecture.thumbnail_image_url,
                'detail_image_url'          : {image.sequence : image.image_url for image in lecture.lectureimage_set.all()},
                'user_status'               : user_status, 
                'reviews_info' : [
                    {
                        'user'      : review.user.name,
                        'title'     : review.title,
                        'content'   : review.content,
                        'rating'    : review.rating,
                        'image_url' : [image.image_url for image in review.reviewimage_set.all()]
                    } for review in lecture.review_set.all()],    
            }
            
            return JsonResponse({'message' : 'SUCCESS', 'result' : result}, status=200)
        
        except Lecture.DoesNotExist:
            return JsonResponse({'message' : 'LECTURE_NOT_EXIST'}, status=400)
        
class LectureLikeView(View):
    @signin_decorator
    def post(self, request, lecture_id):
        try:
            lecture          = Lecture.objects.get(id=lecture_id)
            user             = request.user
            like, is_created = Like.objects.get_or_create(user=user, lecture=lecture)
            
            if not is_created:
                like.delete()
                return JsonResponse({'message' : 'CANCEL_LIKE'}, status=200)
            
            return JsonResponse({'message' : 'SUCCESS_LIKE'}, status=201)
        
        except Lecture.DoesNotExist:
            return JsonResponse({'message' : 'LECTURE_NOT_EXIST'}, status=400)

class LecturesView(View):    
    @signin_decorator
    def post(self, request):
        try:
            profile        = request.FILES['profile']
            thumbnail       = request.FILES['thumbnail']
            lecture_images = request.FILES.getlist('lecture_images')
            
            user             = request.user
            user.nickname    = request.POST['nickname']
            user.description = request.POST['introduce']
            
            name          = request.POST['name']
            price         = request.POST['price']
            discount_rate = request.POST['discount_rate']
            
            description    = request.POST['description']
            difficulty_id  = request.POST['difficulty_id']
            subcategory_id = request.POST['subcategory_id']
            title          = request.POST['title']

            file_handler = FileUpload(s3_client)
            
            with transaction.atomic():
                uploaded_profile_image_url = file_handler.upload(profile, BUCKET_DIR_PROFILE)

                user.profile_image_url = uploaded_profile_image_url
                user.save()
              
                uploaded_thumbnail_url = file_handler.upload(thumbnail, BUCKET_DIR_THUMBNAIL)
                
                lecture = Lecture.objects.create(
                        name                = name,
                        price               = price,
                        discount_rate       = discount_rate,
                        thumbnail_image_url = uploaded_thumbnail_url,
                        description         = description,
                        user_id             = user.id,
                        difficulty_id       = difficulty_id,
                        subcategory_id      = subcategory_id
                )
                
                bulk_lecture_images = []

                for idx, lecture_image in enumerate(lecture_images):
                
                    uploaded_lecture_image_url = file_handler.upload(lecture_image,BUCKET_DIR_IMAGE)
                
                    bulk_lecture_images.append(LectureImage(
                        title      = title,
                        image_url  = uploaded_lecture_image_url,
                        sequence   = idx + 1,
                        lecture_id = lecture.id
                    ))
                LectureImage.objects.bulk_create(bulk_lecture_images)       
                 
            return JsonResponse({"message" : "success"},status=201)        
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"},status=400)
        except transaction.TransactionManagementError:
            return JsonResponse({'message':'TransactionManagementError'}, status=400)
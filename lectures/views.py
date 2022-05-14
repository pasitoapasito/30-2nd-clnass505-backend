from django.http      import JsonResponse
from django.db        import transaction
from django.views     import View
from django.db.models import Q, Avg, Count

from core.decorator   import public_decorator, signin_decorator
from core.storage     import FileUpload, s3_client
from my_settings      import (
    BUCKET_DIR_THUMBNAIL,
    BUCKET_DIR_IMAGE,
    BUCKET_DIR_PROFILE 
)

from lectures.models  import Lecture, LectureImage
from users.models     import UserLecture, Like

class LecturesView(View):
    @public_decorator
    def get(self, request):
        sort           = request.GET.get('sort', "recent")
        offset         = int(request.GET.get('offset', 0))
        limit          = int(request.GET.get('limit', 16))
        category_id    = request.GET.get('category', None)
        subcategory_id = request.GET.get('subcategory', None)
        difficulty_id  = request.GET.getlist('difficulty', None)
        search         = request.GET.get('search', None)
        user           = request.user
        
        sort_set = {
            "liked"       : "-likes",
            "unlike"      : "likes",
            "best_grade"  : "-star",
            "worst_grade" : "star",
            "recent"      : "-created_at",
            "old"         : "created_at",
            "expensive"   : "-price",
            "cheap"       : "price"
        }

        q = Q()

        if category_id:
            q &= Q(subcategory__category_id = category_id)

        if subcategory_id:
            q &= Q(subcategory_id = subcategory_id)

        if difficulty_id:
            q &= Q(difficulty_id__in = difficulty_id)

        if search:
            q &= Q(name__icontains = search)

        lectures = Lecture.objects\
                          .annotate(likes = Count("like"), star = Avg("review__rating"))\
                          .filter(q)\
                          .order_by(sort_set[sort])[offset : offset + limit]

        result = [
            {
                "id"               : lecture.id,
                "title"            : lecture.name,
                "price"            : int(lecture.price),
                "discount_rate"    : lecture.discount_rate,
                "thumbnail_image"  : lecture.thumbnail_image_url,
                "creator_nickname" : lecture.user.name,
                "liked_count"      : lecture.likes,
                "user_liked"       : Like.objects.filter(user=user, lecture=lecture).exists()
            } for lecture in lectures
        ]

        return JsonResponse({"message" : "SUCCESS", "data" : result, "results" : len(result)}, status = 200)
    
    @signin_decorator
    def post(self, request):
        try:
            profile          = request.FILES['profile']
            thumbnail        = request.FILES['thumbnail']
            lecture_images   = request.FILES.getlist('lecture_images')
            
            user             = request.user
            user.nickname    = request.POST['nickname']
            user.description = request.POST['introduce']
            
            name             = request.POST['name']
            price            = request.POST['price']
            discount_rate    = request.POST['discount_rate']
            
            description      = request.POST['description']
            difficulty_id    = request.POST['difficulty_id']
            subcategory_id   = request.POST['subcategory_id']
            title            = request.POST['title']

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
                'user_name'                 : user.name if user else None,
                'user_email'                : user.email if user else None,
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
                'is_liked'                  : lecture.like_set.filter(user=user).exists(),
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
        
class LectureCreatorView(View):
    @signin_decorator
    def get(self, request):
        user     = request.user
        lectures = Lecture.objects\
                          .filter(user=user)\
                          .select_related('user', 'subcategory')\
                          .prefetch_related('like_set')
        
        results = [
            {
                'id'                        : lecture.id,
                'user_name'                 : user.name,
                'user_email'                : user.email,
                'subcategory'               : lecture.subcategory.name,
                'creator_nickname'          : lecture.user.nickname,
                'creator_profile_image_url' : lecture.user.profile_image_url,
                'title'                     : lecture.name,
                'price'                     : lecture.price,
                'discount_rate'             : lecture.discount_rate if lecture.discount_rate else None,
                'discount_price'            : float(lecture.price) * (1-(lecture.discount_rate/100))\
                                              if lecture.discount_rate else None,
                'likes'                     : lecture.like_set.count(),
                'thumbnail_image_url'       : lecture.thumbnail_image_url,
            }
        for lecture in lectures]
        
        return JsonResponse({'message' : 'SUCCESS', 'results' : results}, status=200)
        
class LectureStudentView(View):
    @signin_decorator
    def get(self, request):
        user    = request.user
        
        results = [
            {
                'id'                        : lecture.id,
                'user_name'                 : user.name,
                'user_email'                : user.email,
                'subcategory'               : lecture.subcategory.name,
                'creator_nickname'          : lecture.user.nickname,
                'creator_profile_image_url' : lecture.user.profile_image_url,
                'title'                     : lecture.name,
                'price'                     : lecture.price,
                'discount_rate'             : lecture.discount_rate if lecture.discount_rate else None,
                'discount_price'            : float(lecture.price) * (1-(lecture.discount_rate/100))\
                                              if lecture.discount_rate else None,
                'likes'                     : lecture.like_set.count(),
                'is_liked'                  : lecture.like_set.filter(user=user).exists(),
                'thumbnail_image_url'       : lecture.thumbnail_image_url,
            }
        for lecture in user.lectures.all().select_related('subcategory', 'user').prefetch_related('like_set')]
        
        return JsonResponse({'message' : 'SUCCESS', 'results' : results}, status=200)
        
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

    @signin_decorator
    def get(self, request):
        user    = request.user
        likes   = Like.objects\
                      .filter(user=user)\
                      .select_related('user', 'lecture')
        
        results = [
            {
                'id'                        : like.lecture.id,
                'user_name'                 : user.name,
                'user_email'                : user.email,
                'subcategory'               : like.lecture.subcategory.name,
                'creator_nickname'          : like.lecture.user.nickname,
                'creator_profile_image_url' : like.lecture.user.profile_image_url,
                'title'                     : like.lecture.name,
                'price'                     : like.lecture.price,
                'discount_rate'             : like.lecture.discount_rate if like.lecture.discount_rate else None,
                'discount_price'            : float(like.lecture.price) * (1-(like.lecture.discount_rate/100))\
                                              if like.lecture.discount_rate else None,
                'likes'                     : like.lecture.like_set.count(),
                'thumbnail_image_url'       : like.lecture.thumbnail_image_url,
            }
        for like in likes]
    
        return JsonResponse({'message' : 'SUCCESS', 'results' : results}, status=200)

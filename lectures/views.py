from django.views     import View
from django.http      import JsonResponse
from django.db.models import Avg

from lectures.models  import Lecture
from users.models     import UserLecture, Like
from core.decorator   import public_decorator, signin_decorator

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
import jwt

from datetime        import datetime, timedelta
from django.test     import TestCase, Client
from django.conf     import settings

from users.models    import User, UserLecture, Like
from lectures.models import Lecture, Difficulty, Category, Subcategory, LectureImage
from reviews.models  import Review, ReviewImage

class LectureListTest(TestCase):

    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            id = 1,
            name = 'user1',
            nickname = 'test.user1',
            kakao_id = 1,
            email = 'user1@gmail.com',
            description = 'testcode1',
            profile_image_url = 'http://test1.img.jpg',
            point = 1000000
        )

        User.objects.create(
            id = 2,
            name = 'user2',
            nickname = 'test.user2',
            kakao_id = 2,
            email = 'user2@gmail.com',
            description = 'testcode2',
            profile_image_url = 'http://test2.img.jpg',
            point = 1000000
        )

        Category.objects.create(
            id = 1,
            name = 'test.category1'
        )

        Subcategory.objects.create(
            id = 1,
            name = 'test.subcategory1',
            category_id = 1
        )

        Subcategory.objects.create(
            id = 2,
            name = 'test.subcategory2',
            category_id = 1
        )

        Difficulty.objects.create(
            id = 1,
            name = 'difficulty1'
        )

        Difficulty.objects.create(
            id = 2,
            name = 'difficulty2'
        )

        Lecture.objects.create(
            id = 1,
            name = 'test.lecture1',
            price = 30000,
            discount_rate = 20,
            thumbnail_image_url = 'test.thumbnail1.img.jpg',
            description = 'test.lecture1!',
            user_id = 1,
            difficulty_id = 1,
            subcategory_id = 1
        )

        Lecture.objects.create(
            id = 2,
            name = 'test.lecture2',
            price = 20000,
            discount_rate = 20,
            thumbnail_image_url = 'test.thumbnail2.img.jpg',
            description = 'test.lecture2!',
            user_id = 2,
            difficulty_id = 2,
            subcategory_id = 2
        )

        Review.objects.create(
            id = 1,
            title = 'test1',
            content = 'test.review1',
            rating = 4,
            user_id = 1,
            lecture_id = 1
        )

        Review.objects.create(
            id = 2,
            title = 'test2',
            content = 'test.review2',
            rating = 3,
            user_id = 2,
            lecture_id = 2
        )

        Like.objects.create(
            id = 1,
            lecture_id = 2,
            user_id = 2
        )

    def test_success_lectures(self):
        client = Client()
        response = client.get('/lectures')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message' : 'SUCCESS',
                'results' : 2,
                'data'  : [{
                    'id'               : 2,
                    'title'            : 'test.lecture2',
                    'price'            : 20000,
                    'discount_rate'    : 20,
                    'thumbnail_image'  : 'test.thumbnail2.img.jpg',
                    'creator_nickname' : 'user2',
                    'liked_count'      : 1,
                    'user_liked'       : False
                },{
                    'id'               : 1,
                    'title'            : 'test.lecture1',
                    'price'            : 30000,
                    'discount_rate'    : 20,
                    'thumbnail_image'  : 'test.thumbnail1.img.jpg',
                    'creator_nickname' : 'user1',
                    'liked_count'      : 0,
                    'user_liked'       : False
                }]
            }
        )

class LectureDetailTest(TestCase):
    
    maxDiff = None
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            id                = 1,
            name              = 'DGK1',
            nickname          = 'TESTDGK1',
            kakao_id          = 123456789,
            email             = 'test1@gmail.com',
            description       = '테스트코드를 위한 유저입니다.',
            profile_image_url = 'http://test@image1.jpg',
            point             = 1000000
        )
        
        User.objects.create(
            id                = 2,
            name              = 'DGK2',
            nickname          = 'TESTDGK2',
            kakao_id          = 12345678910,
            email             = 'test2@gmail.com',
            description       = '테스트코드를 위한 유저입니다.',
            profile_image_url = 'http://test@image2.jpg',
            point             = 1000000
        )
        
        User.objects.create(
            id                = 3,
            name              = 'DGK3',
            nickname          = 'TESTDGK3',
            kakao_id          = 1234567891011,
            email             = 'test3@gmail.com',
            description       = '테스트코드를 위한 유저입니다.',
            profile_image_url = 'http://test@image3.jpg',
            point             = 1000000
        )

        Category.objects.create(
            id   = 1,
            name = '테스트 카테고리'
        )
        
        Difficulty.objects.create(
            id   = 1,
            name = '테스트'
        )
        
        Subcategory.objects.create(
            id          = 1,
            name        = '테스트 서브카테고리',
            category_id = 1
        )
        
        Lecture.objects.create(
            id                  = 1,
            name                = '테스트용 강의',
            price               = 1000000,
            discount_rate       = 30,
            thumbnail_image_url = 'http://test@thumb_image.jpg',
            description         = '테스트 강의 제공자',
            user_id             = 3,
            difficulty_id       = 1,
            subcategory_id      = 1
        )
        
        Lecture.objects.create(
            id                  = 2,
            name                = '테스트용 강의2',
            price               = 1000000,
            discount_rate       = 30,
            thumbnail_image_url = 'http://test@thumb_image2.jpg',
            description         = '테스트 강의 제공자2',
            user_id             = 1,
            difficulty_id       = 1,
            subcategory_id      = 1,
        )
        
        LectureImage.objects.create(
            id         = 1,
            title      = '상세 이미지',
            image_url  = 'http://test@detail_image.jpg',
            sequence   = 1,
            lecture_id = 1
        )
        
        UserLecture.objects.create(
            id         = 1,
            user_id    = 2,
            lecture_id = 1
        )
        
        UserLecture.objects.create(
            id         = 2,
            user_id    = 3,
            lecture_id = 2
        )
        
        Like.objects.create(
            id         = 1,
            user_id    = 3,
            lecture_id = 1
        )
        
        Review.objects.create(
            id         = 1,
            title      = '테스트용 리뷰',
            content    = '테스트 리뷰입니다.',
            rating     = 5,
            user_id    = 3,
            lecture_id = 1
        )
        
        ReviewImage.objects.create(
            id        = 1,
            image_url = 'http://test@review_image.jpg',
            review_id = 1
        )
        
    def test_lecture_detail_no_token_success(self):
        client   = Client()
        response = client.get('/lectures/1')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'message' : 'SUCCESS',
                'result'  : {
                    'id'                        : 1,
                    'user_name'                 : None,
                    'user_email'                : None,
                    'subcategory'               : '테스트 서브카테고리',
                    'creator_nickname'          : 'TESTDGK3',
                    'creator_profile_image_url' : 'http://test@image3.jpg',
                    'title'                     : '테스트용 강의',
                    'price'                     : '1000000.00',
                    'discount_rate'             : 30,
                    'discount_price'            : 700000.0,
                    'description'               : '테스트 강의 제공자',
                    'difficulty'                : '테스트',
                    'review_avg_rating'         : 5.0,
                    'likes'                     : 1,
                    'is_liked'                  : False,
                    'thumbnail_image_url'       : 'http://test@thumb_image.jpg',
                    'detail_image_url'          : {'1' : 'http://test@detail_image.jpg'},
                    'user_status'               : None,
                    'reviews_info'              : [
                        {
                            'user'      : 'DGK3',
                            'title'     : '테스트용 리뷰',
                            'content'   : '테스트 리뷰입니다.',
                            'rating'    : 5,
                            'image_url' : [
                                'http://test@review_image.jpg'
                            ]
                        }
                    ]
                }
            }
        )
    
    def test_lecture_detail_token_creator_success(self):
        client = Client()
        
        access_token = jwt.encode({'user_id' : 3, 'exp': datetime.utcnow() + timedelta(hours=24)}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {'HTTP_Authorization' : access_token}
        response     = client.get('/lectures/1', **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'message' : 'SUCCESS',
                'result'  : {
                    'id'                        : 1,
                    'user_name'                 : 'DGK3',
                    'user_email'                : 'test3@gmail.com',
                    'subcategory'               : '테스트 서브카테고리',
                    'creator_nickname'          : 'TESTDGK3',
                    'creator_profile_image_url' : 'http://test@image3.jpg',
                    'title'                     : '테스트용 강의',
                    'price'                     : '1000000.00',
                    'discount_rate'             : 30,
                    'discount_price'            : 700000.0,
                    'description'               : '테스트 강의 제공자',
                    'difficulty'                : '테스트',
                    'review_avg_rating'         : 5.0,
                    'likes'                     : 1,
                    'is_liked'                  : True,
                    'thumbnail_image_url'       : 'http://test@thumb_image.jpg',
                    'detail_image_url'          : {'1' : 'http://test@detail_image.jpg'},
                    'user_status'               : 'creator',
                    'reviews_info'              : [
                        {
                            'user'      : 'DGK3',
                            'title'     : '테스트용 리뷰',
                            'content'   : '테스트 리뷰입니다.',
                            'rating'    : 5,
                            'image_url' : [
                                'http://test@review_image.jpg'
                            ]
                        }
                    ]
                }
            }
        )
    
    def test_lecture_detail_token_student_success(self):
        client = Client()
        
        access_token = jwt.encode({'user_id' : 3, 'exp': datetime.utcnow() + timedelta(hours=24)}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {'HTTP_Authorization' : access_token}
        response     = client.get('/lectures/2', **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'message' : 'SUCCESS',
                'result'  : {
                    'id'                        : 2,
                    'user_name'                 : 'DGK3',
                    'user_email'                : 'test3@gmail.com',
                    'subcategory'               : '테스트 서브카테고리',
                    'creator_nickname'          : 'TESTDGK1',
                    'creator_profile_image_url' : 'http://test@image1.jpg',
                    'title'                     : '테스트용 강의2',
                    'price'                     : '1000000.00',
                    'discount_rate'             : 30,
                    'discount_price'            : 700000.0,
                    'description'               : '테스트 강의 제공자2',
                    'difficulty'                : '테스트',
                    'review_avg_rating'         : None,
                    'likes'                     : 0,
                    'is_liked'                  : False,
                    'thumbnail_image_url'       : 'http://test@thumb_image2.jpg',
                    'detail_image_url'          : {},
                    'user_status'               : 'student',
                    'reviews_info'              : []
                }
            }
        )
    
    def test_lecture_detail_token_potential_student_success(self):
        client = Client()
        
        access_token = jwt.encode({'user_id' : 1, 'exp': datetime.utcnow() + timedelta(hours=24)}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {'HTTP_Authorization' : access_token}
        response     = client.get('/lectures/1', **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'message' : 'SUCCESS',
                'result'  : {
                    'id'                        : 1,
                    'user_name'                 : 'DGK1',
                    'user_email'                : 'test1@gmail.com',
                    'subcategory'               : '테스트 서브카테고리',
                    'creator_nickname'          : 'TESTDGK3',
                    'creator_profile_image_url' : 'http://test@image3.jpg',
                    'title'                     : '테스트용 강의',
                    'price'                     : '1000000.00',
                    'discount_rate'             : 30,
                    'discount_price'            : 700000.0,
                    'description'               : '테스트 강의 제공자',
                    'difficulty'                : '테스트',
                    'review_avg_rating'         : 5.0,
                    'likes'                     : 1,
                    'is_liked'                  : False,
                    'thumbnail_image_url'       : 'http://test@thumb_image.jpg',
                    'detail_image_url'          : {'1' : 'http://test@detail_image.jpg'},
                    'user_status'               : 'potential_student',
                    'reviews_info'              : [
                        {
                            'user'      : 'DGK3',
                            'title'     : '테스트용 리뷰',
                            'content'   : '테스트 리뷰입니다.',
                            'rating'    : 5,
                            'image_url' : [
                                'http://test@review_image.jpg'
                            ]
                        }
                    ]
                }
            }
        )
    
    def test_lecture_detail_fail_lecture_not_exist(self):
        client   = Client()
        response = client.get('/lectures/100')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'LECTURE_NOT_EXIST'})
        
class LectureCreatorTest(TestCase):
    
    maxDiff = None
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            id                = 1,
            name              = 'DGK1',
            nickname          = 'TESTDGK1',
            kakao_id          = 123456789,
            email             = 'test1@gmail.com',
            description       = '테스트코드를 위한 유저입니다.',
            profile_image_url = 'http://test@image1.jpg',
            point             = 1000000
        )
        
        User.objects.create(
            id                = 2,
            name              = 'DGK2',
            nickname          = 'TESTDGK2',
            kakao_id          = 12345678910,
            email             = 'test2@gmail.com',
            description       = '테스트코드를 위한 유저입니다.',
            profile_image_url = 'http://test@image2.jpg',
            point             = 1000000
        )
        
        User.objects.create(
            id                = 3,
            name              = 'DGK3',
            nickname          = 'TESTDGK3',
            kakao_id          = 1234567891011,
            email             = 'test3@gmail.com',
            description       = '테스트코드를 위한 유저입니다.',
            profile_image_url = 'http://test@image3.jpg',
            point             = 1000000
        )

        Category.objects.create(
            id   = 1,
            name = '테스트 카테고리'
        )
        
        Difficulty.objects.create(
            id   = 1,
            name = '테스트'
        )
        
        Subcategory.objects.create(
            id          = 1,
            name        = '테스트 서브카테고리',
            category_id = 1
        )
        
        Lecture.objects.create(
            id                  = 1,
            name                = '테스트용 강의',
            price               = 1000000,
            discount_rate       = 30,
            thumbnail_image_url = 'http://test@thumb_image.jpg',
            description         = '테스트 강의 제공자',
            user_id             = 3,
            difficulty_id       = 1,
            subcategory_id      = 1
        )
        
        Lecture.objects.create(
            id                  = 2,
            name                = '테스트용 강의2',
            price               = 1000000,
            discount_rate       = 30,
            thumbnail_image_url = 'http://test@thumb_image2.jpg',
            description         = '테스트 강의 제공자2',
            user_id             = 1,
            difficulty_id       = 1,
            subcategory_id      = 1,
        )
        
        LectureImage.objects.create(
            id         = 1,
            title      = '상세 이미지',
            image_url  = 'http://test@detail_image.jpg',
            sequence   = 1,
            lecture_id = 1
        )
        
        UserLecture.objects.create(
            id         = 1,
            user_id    = 2,
            lecture_id = 1
        )
        
        Like.objects.create(
            id         = 1,
            user_id    = 2,
            lecture_id = 1
        )
        
        Review.objects.create(
            id         = 1,
            title      = '테스트용 리뷰',
            content    = '테스트 리뷰입니다.',
            rating     = 5,
            user_id    = 3,
            lecture_id = 1
        )
        
        ReviewImage.objects.create(
            id        = 1,
            image_url = 'http://test@review_image.jpg',
            review_id = 1
        )
        
    def test_lecture_creator_list_success(self):
        client = Client()
        
        access_token = jwt.encode({'user_id' : 1, 'exp': datetime.utcnow() + timedelta(hours=24)}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {'HTTP_Authorization' : access_token}
        response     = client.get('/lectures/creator', **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'message': 'SUCCESS',
                'results': [
                    {
                        'id'                        : 2,
                        'user_name'                 : 'DGK1',
                        'user_email'                : 'test1@gmail.com',
                        'subcategory'               : '테스트 서브카테고리',
                        'creator_nickname'          : 'TESTDGK1',
                        'creator_profile_image_url' : 'http://test@image1.jpg',
                        'title'                     : '테스트용 강의2',
                        'price'                     : '1000000.00',
                        'discount_rate'             : 30,
                        'discount_price'            : 700000.0,
                        'likes'                     : 0,
                        'thumbnail_image_url'       : 'http://test@thumb_image2.jpg'
                    }
                ]
            }
        )
    
class LectureStudentTest(TestCase):
    
    maxDiff = None
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            id                = 1,
            name              = 'DGK1',
            nickname          = 'TESTDGK1',
            kakao_id          = 123456789,
            email             = 'test1@gmail.com',
            description       = '테스트코드를 위한 유저입니다.',
            profile_image_url = 'http://test@image1.jpg',
            point             = 1000000
        )
        
        User.objects.create(
            id                = 2,
            name              = 'DGK2',
            nickname          = 'TESTDGK2',
            kakao_id          = 12345678910,
            email             = 'test2@gmail.com',
            description       = '테스트코드를 위한 유저입니다.',
            profile_image_url = 'http://test@image2.jpg',
            point             = 1000000
        )
        
        User.objects.create(
            id                = 3,
            name              = 'DGK3',
            nickname          = 'TESTDGK3',
            kakao_id          = 1234567891011,
            email             = 'test3@gmail.com',
            description       = '테스트코드를 위한 유저입니다.',
            profile_image_url = 'http://test@image3.jpg',
            point             = 1000000
        )

        Category.objects.create(
            id   = 1,
            name = '테스트 카테고리'
        )
        
        Difficulty.objects.create(
            id   = 1,
            name = '테스트'
        )
        
        Subcategory.objects.create(
            id          = 1,
            name        = '테스트 서브카테고리',
            category_id = 1
        )
        
        Lecture.objects.create(
            id                  = 1,
            name                = '테스트용 강의',
            price               = 1000000,
            discount_rate       = 30,
            thumbnail_image_url = 'http://test@thumb_image.jpg',
            description         = '테스트 강의 제공자',
            user_id             = 3,
            difficulty_id       = 1,
            subcategory_id      = 1
        )
        
        Lecture.objects.create(
            id                  = 2,
            name                = '테스트용 강의2',
            price               = 1000000,
            discount_rate       = 30,
            thumbnail_image_url = 'http://test@thumb_image2.jpg',
            description         = '테스트 강의 제공자2',
            user_id             = 1,
            difficulty_id       = 1,
            subcategory_id      = 1,
        )
        
        LectureImage.objects.create(
            id         = 1,
            title      = '상세 이미지',
            image_url  = 'http://test@detail_image.jpg',
            sequence   = 1,
            lecture_id = 1
        )
        
        UserLecture.objects.create(
            id         = 1,
            user_id    = 1,
            lecture_id = 1
        )
        
        Like.objects.create(
            id         = 1,
            user_id    = 2,
            lecture_id = 1
        )
        
        Review.objects.create(
            id         = 1,
            title      = '테스트용 리뷰',
            content    = '테스트 리뷰입니다.',
            rating     = 5,
            user_id    = 3,
            lecture_id = 1
        )
        
        ReviewImage.objects.create(
            id        = 1,
            image_url = 'http://test@review_image.jpg',
            review_id = 1
        )
        
    def test_lecture_student_list_success(self):
        client = Client()
        
        access_token = jwt.encode({'user_id' : 1, 'exp': datetime.utcnow() + timedelta(hours=24)}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {'HTTP_Authorization' : access_token}
        response     = client.get('/lectures/student', **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'message': 'SUCCESS',
                'results': [
                    {
                        'id'                        : 1,
                        'user_name'                 : 'DGK1',
                        'user_email'                : 'test1@gmail.com',
                        'subcategory'               : '테스트 서브카테고리',
                        'creator_nickname'          : 'TESTDGK3',
                        'creator_profile_image_url' : 'http://test@image3.jpg',
                        'title'                     : '테스트용 강의',
                        'price'                     : '1000000.00',
                        'discount_rate'             : 30,
                        'discount_price'            : 700000.0,
                        'likes'                     : 1,
                        'is_liked'                  : False,
                        'thumbnail_image_url'       : 'http://test@thumb_image.jpg'
                    }
                ]
            }
        )

class LectureLikeTest(TestCase):
    
    maxDiff = None
    
    def setUp(self):
        User.objects.create(
            id                = 1,
            name              = 'DGK1',
            nickname          = 'TESTDGK1',
            kakao_id          = 123456789,
            email             = 'test1@gmail.com',
            description       = '테스트코드를 위한 유저입니다.',
            profile_image_url = 'http://test@image1.jpg',
            point             = 1000000
        )

        User.objects.create(
            id                = 2,
            name              = 'DGK2',
            nickname          = 'TESTDGK2',
            kakao_id          = 12345678910,
            email             = 'test2@gmail.com',
            description       = '테스트코드를 위한 유저입니다.',
            profile_image_url = 'http://test@image2.jpg',
            point             = 1000000
        )

        Category.objects.create(
            id   = 1,
            name = '테스트 카테고리'
        )

        Difficulty.objects.create(
            id   = 1,
            name = '테스트'
        )

        Subcategory.objects.create(
            id          = 1,
            name        = '테스트 서브카테고리',
            category_id = 1
        )

        Lecture.objects.create(
            id                  = 1,
            name                = '테스트용 강의',
            price               = 1000000,
            discount_rate       = 30,
            thumbnail_image_url = 'http://test@thumb_image.jpg',
            description         = '테스트 강의 제공자',
            user_id             = 1,
            difficulty_id       = 1,
            subcategory_id      = 1
        )

        LectureImage.objects.create(
            id         = 1,
            title      = '상세 이미지',
            image_url  = 'http://test@detail_image.jpg',
            sequence   = 1,
            lecture_id = 1
        )

        UserLecture.objects.create(
            id         = 1,
            user_id    = 2,
            lecture_id = 1
        )

        Like.objects.create(
            id         = 1,
            user_id    = 2,
            lecture_id = 1
        )

        Review.objects.create(
            id         = 1,
            title      = '테스트용 리뷰',
            content    = '테스트 리뷰입니다.',
            rating     = 5,
            user_id    = 1,
            lecture_id = 1
        )

        ReviewImage.objects.create(
            id        = 1,
            image_url = 'http://test@review_image.jpg',
            review_id = 1
        )

    def tearDown(self):
        User.objects.all().delete()
        Category.objects.all().delete()
        Difficulty.objects.all().delete()
        Subcategory.objects.all().delete()
        Lecture.objects.all().delete()
        LectureImage.objects.all().delete()
        UserLecture.objects.all().delete()
        Like.objects.all().delete()
        Review.objects.all().delete()
        ReviewImage.objects.all().delete()

    def test_lecture_like_create_success(self):
        client = Client()

        access_token = jwt.encode({'user_id' : 1, 'exp': datetime.utcnow() + timedelta(hours=24)}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {'HTTP_Authorization' : access_token}
        response     = client.post('/lectures/1/like', **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'SUCCESS_LIKE'})

    def test_lecture_like_cancel_success(self):
        client = Client()

        access_token = jwt.encode({'user_id' : 2, 'exp': datetime.utcnow() + timedelta(hours=24)}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {'HTTP_Authorization' : access_token}
        response     = client.post('/lectures/1/like', **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'CANCEL_LIKE'})
        
    def test_lecture_like_list_success(self):
        client = Client()
    
        access_token = jwt.encode({'user_id' : 2, 'exp': datetime.utcnow() + timedelta(hours=24)}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {'HTTP_Authorization' : access_token}
        response     = client.get('/lectures/likes', **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "message": "SUCCESS",
                "results": [
                    {
                        "id"                       : 1,
                        "user_name"                : "DGK2",
                        "user_email"               : "test2@gmail.com",
                        "subcategory"              : "테스트 서브카테고리",
                        "creator_nickname"         : 'TESTDGK1',
                        "creator_profile_image_url": "http://test@image1.jpg",
                        "title"                    : "테스트용 강의",
                        "price"                    : "1000000.00",
                        "discount_rate"            : 30,
                        "discount_price"           : 700000.0,
                        "likes"                    : 1,
                        "thumbnail_image_url"      : "http://test@thumb_image.jpg"
                    }
                ]
            }
        )
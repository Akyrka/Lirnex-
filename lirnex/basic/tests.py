from urllib import response
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment

# Create your tests here.

class PostTest(TestCase):
    def test_post_list_case(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200) 

class PostModelTest(TestCase):
    def test_post_model_create(self):
        user = User.objects.create_user(username="testuser", password="123")
        post = Post.objects.create(author =user,caption="Test 1" )
        self.assertEqual(post.caption, "Test 1")
        self.assertEqual(post.author.username, "testuser")

class LikePostSimpleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="123")
        self.post = Post.objects.create(author=self.user, caption="test")

    def test_like_post(self):
        self.client.login(username="test", password="123")

        # Отправляем запрос на лайк
        response = self.client.post(f"/post/{self.post.id}/like/")

        # Проверяем статус
        self.assertEqual(response.status_code, 200)

        # Проверяем, что лайк добавился
        self.post.refresh_from_db()
        self.assertIn(self.user, self.post.likes.all())

class CommentPostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="usertest2", password="123")
        self.post = Post.objects.create(author=self.user, caption='test')

    def test_comment_post(self):
        self.client.login(username="usertest2", password="123")
        
        response = self.client.post(f"/post/{self.post.id}/comment/",{"text":"Коментарій"},follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)

        comment = Comment.objects.first()

        self.assertEqual(comment.text, "Коментарій")
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)



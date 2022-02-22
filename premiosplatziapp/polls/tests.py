"""Polls tests"""

# Utils
import datetime

# Django
from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

# Polls
from .models import Question

class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose
        pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(
            question_text="Wich is your favorite course?",
            pub_date=time
        )
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns False for questions whose
        pub_date is more than 1 day in the past and True in the other
        case"""
        true_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        false_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        true_question = Question(
            question_text="Would this be True?",
            pub_date=true_time
        )
        false_question = Question(
            question_text="Would this be False?",
            pub_date=false_time
        )
        self.assertTrue(true_question.was_published_recently())
        self.assertFalse(false_question.was_published_recently())

    def test_was_published_recently_with_present_questions(self):
        """was_published_recently returns False for questions whose
        pub_date is in the future"""
        time = timezone.now()
        question = Question(
            question_text="Wich is your favorite course?",
            pub_date=time
        )
        self.assertTrue(question.was_published_recently())


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no question exist, an appropiate message is display"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

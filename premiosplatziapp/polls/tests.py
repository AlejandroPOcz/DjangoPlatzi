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
        """was_published_recently() returns False for questions whose
        pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(
            question_text="Wich is your favorite course?",
            pub_date=time
        )
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_past_questions(self):
        """was_published_recently() returns False for questions whose
        pub_date is more than 1 day in the past and True in the other
        case"""
        true_time = timezone.now() - datetime.timedelta(
            hours=23,
            minutes=59,
            seconds=59)
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
        """was_published_recently() returns True for questions whose
        pub_date is in the present"""
        time = timezone.now()
        question = Question(
            question_text="Wich is your favorite course?",
            pub_date=time)
        self.assertTrue(question.was_published_recently())


def create_question(question_text, days):
    """Create a question with the given question_text and published
    the given number of days offset to now

    Args:
        question_text (str): Text of the question
        days (int): Negative for questions published in the past
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(
        pub_date=time,
        question_text=question_text)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no question exist, an appropiate message is display"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_questions_with_future_pub_date(self):
        """Questions with date greater to timezone.now shouldn't be
        displayed"""
        future_question = create_question("Future Question", 1)
        response = self.client.get(reverse('polls:index'))
        self.assertNotIn(
            future_question,
            response.context['latest_question_list'])

    def test_questions_with_past_pub_date(self):
        """Questions with date greater to timezone.now shouldn't be
        displayed"""
        question = create_question("Past Question", -1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            [question],
            response.context['latest_question_list'])

    def test_future_question_and_past_question(self):
        """Even if both (past and future) question exists, only past
        questions are displayed"""
        past_question = create_question(
            question_text="Past Question",
            days=-1)
        future_question = create_question(
            question_text="Future Question",
            days=1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            [past_question],
            response.context['latest_question_list'])
        self.assertNotIn(
            future_question,
            response.context['latest_question_list'])

    def test_two_past_questions(self):
        """The questions index page may display multiple questions"""
        past_question1 = create_question(question_text="Question 1", days=-1)
        past_question2 = create_question(question_text="Question 2", days=-1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            [past_question2, past_question1],
            response.context['latest_question_list'])

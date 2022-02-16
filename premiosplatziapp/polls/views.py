"""Polls Views"""

from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("You are in the main page")


def detail(request, question_id):
    return HttpResponse(f'You are looking the question {question_id}')


def results(request, question_id):
    return HttpResponse(
        f'You are looking the results of question {question_id}'
    )


def vote(request, question_id):
    return HttpResponse(f'You are voting the question {question_id}')
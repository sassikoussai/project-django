from rest_framework.routers import DefaultRouter
from django.urls import path, include

from screening.views import (
    ApplicantViewSet, ResumeViewSet, JobViewSet,
    InterviewViewSet, ScreeningQuestionViewSet,
    ScreeningAnswerViewSet, FeedbackViewSet,
    NotificationViewSet, JobApplicationViewSet
)
from rest_framework import routers
from django.urls import path
from .views import EdgeNodeViewSet, RequestRoutingView

router = routers.DefaultRouter()
router.register(r'edge-nodes', EdgeNodeViewSet, basename='edgenode')

urlpatterns = router.urls + [
    path('route-request/', RequestRoutingView.as_view(), name='route-request'),
]

router = DefaultRouter()
router.register('applicants', ApplicantViewSet, basename='applicant')
router.register('jobs', JobViewSet, basename='job')
router.register('resumes', ResumeViewSet, basename='resume')
router.register('interviews', InterviewViewSet, basename='interview')
router.register('screening-questions', ScreeningQuestionViewSet, basename='screening-question')
router.register('screening-answers', ScreeningAnswerViewSet, basename='screening-answer')
router.register('feedback', FeedbackViewSet, basename='feedback')
router.register('notifications', NotificationViewSet, basename='notification')
router.register('applications', JobApplicationViewSet, basename='application')

app_name = 'screening'

urlpatterns = [
    path('', include(router.urls)),
    ]
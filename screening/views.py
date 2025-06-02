from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    Applicant, Job, Resume, Interview,
    ScreeningQuestion, ScreeningAnswer, Feedback,
    Notification, JobApplication , Recruiter
)
from .serializers import (
    ApplicantSerializer, JobSerializer, ResumeSerializer,
    InterviewSerializer, ScreeningQuestionSerializer,
    ScreeningAnswerSerializer, FeedbackSerializer,
    NotificationSerializer, JobApplicationSerializer , RecruiterSerializer
)
from rest_framework import viewsets
from .models import EdgeNode
from .serializers import EdgeNodeSerializer
from .authentication import EdgeNodeAPIKeyAuthentication
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import EdgeNode, APIRequestLog
from .serializers import EdgeNodeSerializer, APIRequestLogSerializer
import secrets
from rest_framework.views import APIView
from .tasks import deploy_to_flyio
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from django.utils.decorators import method_decorator

@api_view(['POST'])
def trigger_flyio_deploy(request):
    app_name = request.data.get("app_name")
    image_tag = request.data.get("image_tag")
    task = deploy_to_flyio.delay(app_name, image_tag)
    return Response({"task_id": task.id, "status": "Deployment triggered"})

class RequestRoutingView(APIView):
    permission_classes = [EdgeNodeAPIKeyAuthentication]

    def post(self, request):
        # Example: route to the first healthy node (replace with your logic)
        node = EdgeNode.objects.filter(status="healthy").first()
        if not node:
            return Response({"error": "No healthy edge node available."}, status=503)
        # Optionally, log the request
        APIRequestLog.objects.create(
            edge_node=node,
            response_time_ms=0,  # Placeholder
            latitude=node.latitude,
            longitude=node.longitude,
            status_code=200,
            client_ip=request.META.get('REMOTE_ADDR'),
            extra_data=request.data
        )
        return Response({
            "routed_to": node.name,
            "ip_address": node.ip_address,
            "location": {"lat": node.latitude, "lng": node.longitude}
        })

class EdgeNodeViewSet(viewsets.ModelViewSet):
    queryset = EdgeNode.objects.all()
    serializer_class = EdgeNodeSerializer
    permission_classes = [EdgeNodeAPIKeyAuthentication]  

    @method_decorator(csrf_exempt, name='dispatch')
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        # Custom registration logic
        serializer = EdgeNodeSerializer(data=request.data)
        if serializer.is_valid():
            # Generate a secure API key
            api_key = secrets.token_urlsafe(32)
            edge_node = serializer.save(api_key=api_key)
            return Response({
                "message": "Edge node registered successfully.",
                "node": EdgeNodeSerializer(edge_node).data,
                "api_key": api_key
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def resumes(self, request, pk=None):
        applicant = self.get_object()
        resumes = applicant.resumes.all()
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)

    #get applicant that has a given skill
    @action(detail=False, methods=['get'], url_path=r'by_skill/(?P<skill>[^/.]+)')
    def get_developer_by_skill(self, request,skill = None):
        skill = request.query_params.get('skill')
        applicants = Applicant.objects.filter(skills__icontains=skill)
        #
        if not applicants.exists():
            return Response({'message': 'No applicants found with the given skill.'}, status=status.HTTP_204_NO_CONTENT)
        serializer = ApplicantSerializer(applicants, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def update_applicant(self, request, pk=None):
        applicant = self.get_object()
        serializer = ApplicantSerializer(applicant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def get_tunisian_dev(self,request):
        result = ApplicantSerializer(Applicant.objects.filter(
            skills__icontains = 'developer' & Q(phone_number__startswith = '+216')|Q(phone_number__startswith='00216'))
        , many=True).data
        if not result:
            return Response({'message': 'No applicants found with the given skill.'}, status=status.HTTP_204_NO_CONTENT)
        return Response(result, status=status.HTTP_200_OK)


    @action (detail=False, methods=['GET'], url_path='by_age/(?P<birthday>[^/.]+)')
    def get_applicant_by_age(self, request, birthday):
        # Filter applicants by age
        applicants = Applicant.objects.filter(birthday__year__gte=birthday)
        if not applicants.exists():
            return Response({'message': 'No applicants found with the given age.'}, status=status.HTTP_204_NO_CONTENT)
        serializer = ApplicantSerializer(applicants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['POST','PATCH', 'PUT'])
    def affect_or_update_resume(self, request, pk):
        applicant = self.get_object()
        resume_id = request.data.get('resume_id')
        if resume_id:
            try:
                resume = Resume.objects.get(id=resume_id)
                applicant.resumes.add(resume)
                return Response({'status': 'resume added to applicant'})
            except Resume.DoesNotExist:
                return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'resume_id not provided'}, status=status.HTTP_400_BAD_REQUEST)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def applicants(self, request, pk=None):
        job = self.get_object()
        applicants = job.applicants.all()
        serializer = ApplicantSerializer(applicants, many=True)
        return Response(serializer.data)


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user.applicant_profile)


class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes = [permissions.AllowAny]

    #get applicant that got reviewed by a recruiter in a given company with given skill
    @action(detail=False, methods=['get'])
    def get_interview_by_recruiter(self, request):
        skill = request.query_params.get('skill',None)
        company = request.query_params.get('company',None)
        if not skill or not company:
            return Response({'message': 'Please provide both skill and company.'}, status=status.HTTP_400_BAD_REQUEST)

        applicants = Interview.objects.filter(
            Q(applicant__skills__icontains=skill) & Q(job__recruiter__company_name__iexact=company)
        )
        serializer = ApplicantSerializer(applicants, many=True)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No applicants found with the given skill and company.'}, status=status.HTTP_204_NO_CONTENT)

class ScreeningQuestionViewSet(viewsets.ModelViewSet):
    queryset = ScreeningQuestion.objects.all()
    serializer_class = ScreeningQuestionSerializer
    permission_classes = [permissions.AllowAny]


class ScreeningAnswerViewSet(viewsets.ModelViewSet):
    queryset = ScreeningAnswer.objects.all()
    serializer_class = ScreeningAnswerSerializer
    permission_classes = [permissions.AllowAny]


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.AllowAny]


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        notifications.update(is_read=True)
        return Response({'status': 'all notifications marked as read'})

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user.applicant_profile)

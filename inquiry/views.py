from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import viewsets
from .models import Inquiry
from .serializers import InquirySerializer
from .permissions import IsAdminOrCreateOnly

class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    permission_classes = [IsAdminOrCreateOnly]

    def perform_create(self, serializer):
        inquiry = serializer.save()
        email = EmailMessage(
            subject="Inquiry Received",
            body=f"Hello {inquiry.name},\n\nWe have received your inquiry successfully.\n\nYour message:\n{inquiry.message}\n\nThank you for contacting us.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[inquiry.email],
            reply_to=[inquiry.email],
        )
        email.send(fail_silently=False)
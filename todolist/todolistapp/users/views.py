from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from datetime import datetime
from .models import User
from .serializers import UserRegisterSerializer
import logging
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Create User"""
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        """Custom authentication"""
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        logger.debug("IP User : " + str(request.META.get('REMOTE_ADDR')) +
                     " User-Agent: " + str(request.META['HTTP_USER_AGENT']) +
                     " Time: " + str(datetime.now()) +
                     " User id: " + str(user.pk)
                     )

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })
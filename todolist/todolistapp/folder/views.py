from datetime import datetime
from rest_framework import status
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from page.models import StatusAccess
from .serializers import FolderSerializer, FolderAccessSerializer
from .service import *
import logging

logger = logging.getLogger(__name__)


class FolderGetAPIView(APIView):
    serializer_class = FolderSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Get folder with check access"""
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(get_all_folder(request.user, Folder.objects.all()), request)
        serializer = self.serializer_class(result_page, many=True)

        logger.debug("User id: " + str(request.user.id) +
                     " Time: " + str(datetime.now()) +
                     " " + StatusAccess.READ
                     )

        return Response(serializer.data, status=status.HTTP_200_OK)


class FolderAPIView(APIView):
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Create folder with check access"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_folder = Folder.objects.create(
                name=request.data['name'],
                status_access=request.data['status_access'],
                user=request.user
        )

        logger.debug("User id: " + str(request.user.id) +
                     " Time: " + str(datetime.now()) +
                     " Folder id: " + str(new_folder.id) +
                     " " + StatusAccess.CREATE
                     )

        return Response({'folder': FolderSerializer(new_folder).data}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """Delete folder with check access"""
        folder = get_folder(pk)
        if is_users_folder(request.user, folder):
            if not folder.is_delete:
                delete_all_by_folder(folder)
                folder.is_delete = True
                folder.save()

                logger.debug("User id: " + str(request.user.id) +
                             " Time: " + str(datetime.now()) +
                             " Folder id: " + str(folder.id) +
                             " " + StatusAccess.DELETE
                             )

                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Folder is deleted"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "No access"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        """Update folder with check access"""
        folder = get_folder(pk)
        if is_users_folder(request.user, folder):
            if not folder.is_delete:
                serializer = self.serializer_class(data=request.data, instance=folder)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                logger.debug("User id: " + str(request.user.id) +
                             " Time: " + str(datetime.now()) +
                             " Folder id: " + str(folder.id) +
                             " " + StatusAccess.UPDATE
                             )

                return Response({'folder': serializer.data})
            return Response({"error": "Folder is deleted"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "No access"}, status=status.HTTP_403_FORBIDDEN)


class FolderAccessPostAPIView(APIView):
    serializer_class = FolderAccessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """Create FolderAccess"""
        folder = get_folder(pk)
        if is_users_folder(request.user, folder):
            if not folder.is_delete:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)

                new_folder_access = FolderAccess.objects.create(
                        username=request.data['username'],
                        folder=folder
                )

                logger.debug("User id: " + str(request.user.id) +
                             " Time: " + str(datetime.now()) +
                             " FolderAccess id: " + str(new_folder_access.id) +
                             " " + StatusAccess.CREATE
                             )

            else:
                return Response({"error": "Folder is deleted"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "No access"}, status=status.HTTP_403_FORBIDDEN)
        return Response({'folder_access': FolderSerializer(new_folder_access).data}, status=status.HTTP_200_OK)


class FolderAccessDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk: int, username: str):
        """Delete FolderAccess"""
        folder = get_folder(pk)
        if is_users_folder(request.user, folder):
            if not folder.is_delete:
                folder_access = get_folder_access(username)
                if folder_access is None:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                folder_access.delete()

                logger.debug("User id: " + str(request.user.id) +
                             " Time: " + str(datetime.now()) +
                             " FolderAccess id: " + str(folder_access.id) +
                             " " + StatusAccess.DELETE
                             )

                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Folder is deleted"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "No access"}, status=status.HTTP_403_FORBIDDEN)

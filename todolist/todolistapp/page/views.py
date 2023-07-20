from datetime import datetime
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import permissions, status
from .models import Page, PageAccess, StatusAccess
from folder.service import get_folder, is_users_folder
from .service import has_page_access, get_page_access, get_page, get_all_page, delete_all_entry_by_page
import logging


logger = logging.getLogger(__name__)


class PagePostAPIView(APIView):
    serializer_class = PageSerializers
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """Create page and check success"""
        folder = get_folder(pk)
        if has_page_access(folder, request.user, StatusAccess.CREATE):
            if not folder.is_delete:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)

                new_page = Page.objects.create(
                    name=request.data['name'],
                    author_user=request.user.username,
                    update_user=None,
                    folder=folder
                )

                logger.debug("User id: " + str(request.user.id) +
                             " Time: " + str(datetime.now()) +
                             " Page id: " + str(new_page.id) +
                             " " + StatusAccess.READ
                             )

                return Response({'page': PageSerializers(new_page).data}, status=status.HTTP_200_OK)
            return Response({"error": "Folder is deleted"}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'No access'}, status=status.HTTP_404_NOT_FOUND)


class PagePutAPIView(APIView):
    """Update page and check access"""
    serializer_class = PageSerializers
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        page = get_page(pk)
        if has_page_access(page.folder, request.user, StatusAccess.UPDATE):
            if not page.is_delete:
                page.update_user = request.user.username
                serializer = self.serializer_class(data=request.data, instance=page)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                logger.debug("User id: " + str(request.user.id) +
                             " Time: " + str(datetime.now()) +
                             " Page id: " + str(page.id) +
                             " " + StatusAccess.UPDATE
                             )

                return Response({'page': serializer.data})
            return Response({"error": "Page is deleted"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "No access"}, status=status.HTTP_403_FORBIDDEN)


class PageDeleteAPIView(APIView):
    """Delete page and check access"""
    serializer_class = PageSerializers
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        page = get_page(pk)
        if has_page_access(page.folder, request.user, StatusAccess.DELETE):
            if not page.is_delete:
                delete_all_entry_by_page(page)
                page.is_delete = True
                page.save()

                logger.debug("User id: " + str(request.user.id) +
                             " Time: " + str(datetime.now()) +
                             " Page id: " + str(page.id) +
                             " " + StatusAccess.DELETE
                             )

                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Page is deleted"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "No access"}, status=status.HTTP_403_FORBIDDEN)


class PageGetAPIView(APIView):
    serializer_class = PageSerializers
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Get page and check success with pagination"""
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(get_all_page(Page.objects.all(), request.user), request)
        serializer = self.serializer_class(result_page, many=True)

        logger.debug("User id: " + str(request.user.id) +
                     " Time: " + str(datetime.now()) +
                     " " + StatusAccess.READ
                     )

        return Response(serializer.data, status=status.HTTP_200_OK)


class PageAccessAPIView(APIView):
    serializer_class = PageAccessSerializers
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """Create PageAccess"""
        folder = get_folder(pk)
        if is_users_folder(request.user, folder):
            if not folder.is_delete:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)

                new_page_access = PageAccess.objects.create(
                    username=request.data['username'],
                    page_access_status=request.data['page_access_status'],
                    folder=folder
                )

                logger.debug("User id: " + str(request.user.id) +
                             " Time: " + str(datetime.now()) +
                             " PageAccess id: " + str(new_page_access.id) +
                             " " + StatusAccess.CREATE
                             )

                return Response({'page_access': PageAccessSerializers(new_page_access).data}, status=status.HTTP_200_OK)
            return Response({"error": "Folder is deleted"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "No access"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk: int, username: str) -> Response:
        """Delete PageAccess"""
        folder = get_folder(pk)
        if is_users_folder(request.user, folder):
            if not folder.is_delete:
                page_access = get_page_access(folder, username)
                if page_access is not None:
                    page_access.delete()

                    logger.debug("User id: " + str(request.user.id) +
                                 " Time: " + str(datetime.now()) +
                                 " PageAccess id: " + str(page_access.id) +
                                 " " + StatusAccess.DELETE
                                 )

                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"error": "Folder is deleted"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "No access"}, status=status.HTTP_403_FORBIDDEN)


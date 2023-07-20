from datetime import datetime
from rest_framework import permissions, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EntrySerializer, EntryAccessSerializer, EntryLinkSerializer
from .service import has_entry_access, get_entry, get_entry_access, get_all_entry, generate_random_url, get_entry_link
from page.service import get_page
from folder.service import is_users_folder, get_folder
from .models import *
from page.models import StatusAccess
import logging


logger = logging.getLogger(__name__)


class EntryGetAPIView(APIView):
    serializer_class = EntrySerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Get Entry with access check and pagination"""
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(get_all_entry(request.user), request)
        serializer = self.serializer_class(result_page, many=True)

        logger.debug("User id: " + str(request.user.id) +
                     " Time: " + str(datetime.now()) +
                     " " + StatusAccess.READ
                     )

        return Response(serializer.data, status=status.HTTP_200_OK)


class EntryPostAPIView(APIView):
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """Create Entry and check access"""
        page = get_page(pk)
        if has_entry_access(page, request.user, StatusAccess.CREATE):
            if not page.is_delete:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                new_entry = Entry.objects.create(
                    text=request.data['text'],
                    author_user=request.user.username,
                    update_user=None,
                    entry_status=request.data['entry_status'],
                    page=page
                )

                logger.debug("User id: " + str(request.user.id) +
                             " Time: " + str(datetime.now()) +
                             " Entry id: " + str(new_entry.id) +
                             " " + StatusAccess.CREATE
                             )

                return Response({'entry': EntrySerializer(new_entry).data}, status=status.HTTP_200_OK)
            return Response({"error": "Page is deleted"}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'No access'}, status=status.HTTP_404_NOT_FOUND)


class EntryPutAPIView(APIView):
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        """Update Entry and Create EntryLink with check access"""
        entry = get_entry(pk)
        if has_entry_access(entry.page, request.user, StatusAccess.UPDATE):
            if not entry.is_delete:
                entry.update_user = request.user.username

                EntryLink.objects.create(
                    entry=entry,
                    text=entry.text,
                    url=generate_random_url()
                )

                serializer = self.serializer_class(data=request.data, instance=entry)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                logger.debug("User id: " + str(request.user.id) +
                             " Time: " + str(datetime.now()) +
                             " Entry id: " + str(entry.id) +
                             " " + StatusAccess.UPDATE
                             )

                return Response({'entry': serializer.data})
            return Response({"error": "Entry is deleted"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "No access"}, status=status.HTTP_403_FORBIDDEN)


class EntryDeleteAPIView(APIView):
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        """Delete Entry and check access"""
        entry = get_entry(pk)
        if has_entry_access(entry.page, request.user, StatusAccess.DELETE):
            if not entry.is_delete:
                entry.is_delete = True
                entry.save()

                logger.debug("User id: " + str(request.user.id) +
                             " Time: " + str(datetime.now()) +
                             " Entry id: " + str(entry.id) +
                             " " + StatusAccess.DELETE
                             )

                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Entry is deleted"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "No access"}, status=status.HTTP_403_FORBIDDEN)


class EntryAccessAPIView(APIView):
    serializer_class = EntryAccessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """Create EntryAccess with check access"""
        folder = get_folder(pk)
        if is_users_folder(request.user, folder):
            if not folder.is_delete:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)

                new_entry_access = EntryAccess.objects.create(
                        username=request.data['username'],
                        entry_access_status=request.data['entry_access_status'],
                        folder=folder
                )

                logger.debug("User id: " + str(request.user.id) +
                             " Time: " + str(datetime.now()) +
                             " EntryAccess id: " + str(new_entry_access.id) +
                             " " + StatusAccess.CREATE
                             )

                return Response({'entry_access': EntryAccessSerializer(new_entry_access).data}, status=status.HTTP_200_OK)
            return Response({"error": "Folder is deleted"}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'No access'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, username: str) -> Response:
        """Delete EntryAccess with check access"""
        folder = get_folder(pk)
        if is_users_folder(request.user, folder):
            if not folder.is_delete:
                entry_access = get_entry_access(username)
                if entry_access is not None:
                    entry_access.delete()

                    logger.debug("User id: " + str(request.user.id) +
                                 " Time: " + str(datetime.now()) +
                                 " EntryAccess id: " + str(folder.id) +
                                 " " + StatusAccess.DELETE
                                 )

                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"error": "Folder is deleted"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "No access"}, status=status.HTTP_403_FORBIDDEN)


class EntryLinkAPIView(APIView):
    serializer_class = EntryLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, url: str) -> Response:
        """Get EntryLink"""
        entry_link = get_entry_link(url)
        if entry_link is not None:
            serializer = self.serializer_class(entry_link)

            logger.debug("User id: " + str(request.user.id) +
                         " Time: " + str(datetime.now()) +
                         " EntryLink id: " + str(entry_link.id) +
                         " " + StatusAccess.READ
                         )

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Entry link not found"}, status=status.HTTP_404_NOT_FOUND)

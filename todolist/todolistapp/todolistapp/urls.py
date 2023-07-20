"""
URL configuration for todolistapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from users.views import RegisterUserView, CustomAuthToken
from folder.views import FolderGetAPIView, FolderAPIView, FolderAccessPostAPIView, FolderAccessDeleteAPIView
from page.views import PageAccessAPIView, PagePostAPIView, PagePutAPIView, PageDeleteAPIView, PageGetAPIView
from entry.views import EntryAccessAPIView, EntryPostAPIView, EntryGetAPIView, EntryPutAPIView, EntryDeleteAPIView, EntryLinkAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/register/', RegisterUserView.as_view(), name='register'),
    # path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/', CustomAuthToken.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/v1/folder/get/', FolderGetAPIView.as_view(), name='folder_get'),
    path('api/v1/folder/post/', FolderAPIView.as_view(), name='folder_post'),
    path('api/v1/folder/put/<int:pk>/', FolderAPIView.as_view(), name='folder_put'),
    path('api/v1/folder/delete/<int:pk>/', FolderAPIView.as_view(), name='folder_delete'),
    path('api/v1/folder/setrole/<int:pk>/', FolderAccessPostAPIView.as_view(), name='folder_access_post'),
    path('api/v1/folder/deleterole/<int:pk>/<str:username>/', FolderAccessDeleteAPIView.as_view(), name='folder_access_delete'),

    path('api/v1/page/get/', PageGetAPIView.as_view(), name='page_get'),
    path('api/v1/page/post/<int:pk>/', PagePostAPIView.as_view(), name='page_post'),
    path('api/v1/page/put/<int:pk>/', PagePutAPIView.as_view(), name='page_put'),
    path('api/v1/page/delete/<int:pk>/', PageDeleteAPIView.as_view(), name='page_delete'),
    path('api/v1/page/setrole/<int:pk>/', PageAccessAPIView.as_view(), name='page_access_post'),
    path('api/v1/page/deleterole/<int:pk>/<str:username>/', PageAccessAPIView.as_view(), name='page_access_delete'),

    path('api/v1/entry/get/', EntryGetAPIView.as_view(), name='entry_get'),
    path('api/v1/entry/post/<int:pk>/', EntryPostAPIView.as_view(), name='entry_post'),
    path('api/v1/entry/put/<int:pk>/', EntryPutAPIView.as_view(), name='entry_put'),
    path('api/v1/entry/delete/<int:pk>/', EntryDeleteAPIView.as_view(), name='entry_delete'),
    path('api/v1/entry/setrole/<int:pk>/', EntryAccessAPIView.as_view(), name='entry_access_post'),
    path('api/v1/entry/deleterole/<int:pk>/<str:username>/', EntryAccessAPIView.as_view(), name='entry_access_delete'),
    path('api/v1/entry/link/<str:url>/', EntryLinkAPIView.as_view(), name='entry_link_get'),
]

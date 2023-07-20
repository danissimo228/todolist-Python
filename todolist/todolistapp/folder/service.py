from django.db.models import QuerySet
from django.http import Http404
from folder.models import Folder, FolderAccess
from users.models import User
from page.models import Page
from entry.models import Entry


def is_users_folder(user: User, folder: Folder) -> bool:
    return folder.user == user


def check_folder_access(user: User, folder: Folder) -> bool:
    if folder.is_delete:
        return False
    if not folder.status_access:
        for folder_access in list(FolderAccess.objects.all()):
            if folder_access.username == user.username and folder_access.folder == folder:
                return True
    return is_users_folder(user, folder) or folder.status_access


def get_folder(pk: int) -> Folder:
    try:
        return Folder.objects.get(pk=pk)
    except Folder.DoesNotExist:
        raise Http404


def get_folder_access(username: str) -> FolderAccess:
    for folder_access in FolderAccess.objects.all():
        if folder_access.username == username:
            return folder_access


def get_all_folder(user: User, queryset: QuerySet) -> QuerySet:
    lst_of_folders = []
    for folder in list(queryset):
        if folder.status_access and not folder.is_delete:
            lst_of_folders.append(folder)
        if folder.user == user and not folder.is_delete:
            lst_of_folders.append(folder)
        if not folder.status_access and not folder.is_delete:
            if check_folder_access(user, folder):
                lst_of_folders.append(folder)
    lst_of_folders = list(set(lst_of_folders))
    lst_of_id_folder = [getattr(p, "id") for p in lst_of_folders]
    return Folder.objects.filter(id__in=lst_of_id_folder)


def get_all_page_by_folder(folder: Folder) -> list:
    lst_of_page = []
    for page in list(Page.object.all()):
        if page.folder == folder:
            page.is_delete = True
            page.save()
            lst_of_page.append(page)
    return lst_of_page


def get_all_entry_by_page(lst_of_page: list) -> list:
    lst_of_entry = []
    for entry in Entry.objects.all():
        for page in lst_of_page:
            if entry.page == page:
                entry.is_delete = True
                entry.save()
                lst_of_entry.append(entry)
    return lst_of_entry


def delete_all_by_folder(folder: Folder) -> None:
    get_all_entry_by_page(get_all_page_by_folder(folder))

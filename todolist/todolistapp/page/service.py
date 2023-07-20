from folder.service import *
from .models import *


def has_page_access(folder: Folder, user: User, status: str) -> bool:
    if is_users_folder(user, folder):
        return True
    if check_folder_access(user, folder):
        page_access = find_page_access(user)
        return page_access is not None and page_access.page_access_status == status and page_access.folder == folder
    else:
        return False


def find_page_access(user: User) -> PageAccess:
    for page_access in list(PageAccess.objects.all()):
        if page_access.username == user.username:
            return page_access


def get_page_access(folder: Folder, username: str) -> PageAccess:
    for page_access in PageAccess.objects.all():
        if page_access.folder == folder and page_access.username == username:
            return page_access


def get_page(pk: int) -> Page:
    try:
        return Page.objects.get(pk=pk)
    except Page.DoesNotExist:
        raise Http404


def get_all_page(queryset: QuerySet, user: User) -> QuerySet:
    lst_of_page = []
    for page in list(queryset):
        if page.folder.status_access:
            lst_of_page.append(page)
        if has_page_access(page.folder, user, StatusAccess.READ) and not page.is_delete:
            lst_of_page.append(page)
    lst_of_page = list(set(lst_of_page))
    lst_of_id_page = [getattr(p, "id") for p in lst_of_page]
    return Page.objects.filter(id__in=lst_of_id_page)


def delete_all_entry_by_page(page: Page) -> None:
    delete_all_entry_by_page(page)

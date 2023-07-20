from django.db.models import QuerySet
from django.http import Http404
from folder.models import Folder
from page.models import Page
from users.models import User
from page.service import find_page_access
from page.models import StatusAccess
from .models import EntryAccess, Entry, EntryLink
from folder.service import is_users_folder, check_folder_access
import uuid


def has_entry_access(page: Page, user: User, status: str) -> bool:
    """Check Entry access"""
    if is_users_folder(user, page.folder):
        return True
    if has_page_access_for_entry(user, page.folder):
        entry_access = get_entry_access(user.username)
        print(entry_access.entry_access_status)
        return entry_access is not None and entry_access.entry_access_status == status and entry_access.folder == page.folder


def has_page_access_for_entry(user: User, folder: Folder) -> bool:
    if is_users_folder(user, folder):
        return True
    if check_folder_access(user, folder):
        page_access = find_page_access(user)
        return page_access is not None and page_access.folder == folder
    else:
        return False


def get_entry(pk: int) -> Entry:
    try:
        return Entry.objects.get(pk=pk)
    except Entry.DoesNotExist:
        raise Http404


def get_entry_access(username: str) -> EntryAccess:
    for entry_access in EntryAccess.objects.all():
        if entry_access.username == username:
            return entry_access


def get_all_entry(user: User) -> QuerySet:
    lst_of_entry = []
    for entry in list(Entry.objects.all()):
        if entry.page.folder.status_access:
            lst_of_entry.append(entry)
        if has_entry_access(entry.page, user, StatusAccess.READ):
            lst_of_entry.append(entry)

    lst_of_entry = list(set(lst_of_entry))
    lst_of_id_entry = [getattr(e, "id") for e in lst_of_entry]
    return Entry.objects.filter(id__in=lst_of_id_entry)


def generate_random_url() -> str:
    return str(uuid.uuid4())[:11].upper()


def get_entry_link(url: str) -> EntryLink:
    for entry_link in EntryLink.objects.all():
        if entry_link.url == url:
            return entry_link


from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError
from django.core.management import call_command
from django.core.management.base import BaseCommand

from townsquare.models import initial_event_location

###########################
# Permissions
###########################


APP_NAME = 'townsquare'

def get_ct(content_name):
    result = ContentType.objects.filter(app_label=APP_NAME, name=content_name)
    if not result:
        raise Exception('No such content type exists.')
    else:
        return result[0]

def get_perm_by_ct(contenttype):
    return Permission.objects.filter(content_type__in=contenttype)

def create_new_group(name, ct_names):

    group, _ = Group.objects.get_or_create(name=name)

    group_cts = []
    group_perms = []

    for ct_name in ct_names:
        group_cts.append(get_ct(ct_name))

    for perm in get_perm_by_ct(group_cts):
        group_perms.append(perm)

    group.permissions.add(*group_perms) 
    group.save()


class Command(BaseCommand):

    args = "No args accepted for now"
    help = "Initializes Townsquare permission groups"

    def handle(self, *args, **options):
        
        # create permission groups
        create_new_group('Staff', ('session', 'event', 'event location', 'volunteer'))
        create_new_group('Admin', ('session', 'event', 'event location'))
        create_new_group('Volunteer', ())

        # create initial event location
        initial_event_location()






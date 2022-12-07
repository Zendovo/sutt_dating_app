from django_tables2 import tables
from user.models import UserProfile

class UserProfilesTables(tables.Table):
    class Meta:
        model = UserProfile
        sequence = ('id', 'first_name', 'last_name', 'user', 'age', 'gender', 'preference', 'image', 'about')
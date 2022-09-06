# from django.conf import settings
# from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth.hashers import check_password
# from django.contrib.auth.models import User
# from rest_framework.authentication import TokenAuthentication
# class RedmineAuthBackend(BaseBackend):
#     """
#     Authenticate against the redmine database.
#
#     Use the login name and a hash of the password. For example:
#
#     ADMIN_LOGIN = 'admin'
#     ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
#     """
#
#     # redmine_key = attrs.get('redmine_key')
#     # try:
#     #
#     #
#
#     def authenticate(self, request, username=None, redmine_key=None):
#
#         try:
#             username = attrs.get('username')
#             redmine_key = attrs.get('redmine_key')
#             hd_user = HelpdeskUser.objects.get(login=username, redminetoken__value=redmine_key)
#         except HelpdeskUser.DoesNotExist:
#             return None
#
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             # Create a new user. There's no need to set a password
#             # because only the password from settings.py is checked.
#             user = User(username=username)
#             if hd_user.admin == 1:
#                 user.is_staff = True
#                 user.is_superuser = True
#             user.save()
#         return user
#
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None
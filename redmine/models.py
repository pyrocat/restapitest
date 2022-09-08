from django.db import models


# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=254)
    description = models.CharField(max_length=254, blank=True, null=True)
    is_public = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'Projects'


class HelpdeskUser(models.Model):
    login = models.CharField(unique=True, max_length=150)
    firstname = models.CharField(blank=True, null=True, max_length=150)
    lastname = models.CharField(blank=True, null=True, max_length=150)
    admin = models.BooleanField()
    status = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'HelpDeskUser'

    def __str__(self):
        return self.login


class Member(models.Model):
    user = models.ForeignKey(HelpdeskUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'Members'


class Role(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    class Meta:
        managed = False
        db_table = 'Roles'


class MemberRole(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'MemberRoles'


class RedmineToken(models.Model):
    user = models.OneToOneField(HelpdeskUser, on_delete=models.CASCADE)
    action = models.TextField(blank=True, null=True)
    value = models.TextField()
    created_on = models.DateTimeField(db_column='created on')  # Field renamed to remove unsuitable characters.
    updated_on = models.DateTimeField(db_column='updated on')  # Field renamed to remove unsuitable characters.
    someother = models.TextField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'Tokens'



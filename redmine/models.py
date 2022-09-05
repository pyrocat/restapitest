from django.db import models

# Create your models here.


class Helpdeskuser(models.Model):
    login = models.CharField(unique=True, max_length=150)
    firstname = models.CharField(blank=True, null=True, max_length=150)
    lastname = models.CharField(blank=True, null=True, max_length=150)
    admin = models.BooleanField()
    status = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'HelpDeskUser'


class Memberroles(models.Model):
    member = models.ForeignKey('Members', on_delete=models.CASCADE)
    role = models.ForeignKey('Roles', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'MemberRoles'


class Members(models.Model):
    user = models.ForeignKey(Helpdeskuser, on_delete=models.CASCADE)
    project = models.ForeignKey('Projects', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'Members'


class Projects(models.Model):
    name = models.CharField(max_length=254)
    description = models.CharField(max_length=254, blank=True, null=True)
    is_public = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'Projects'


class Roles(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'Roles'


class Tokens(models.Model):
    user = models.ForeignKey(Helpdeskuser, on_delete=models.CASCADE)
    action = models.TextField(blank=True, null=True)
    value = models.TextField()
    created_on = models.DateTimeField(db_column='created on')  # Field renamed to remove unsuitable characters.
    updated_on = models.DateTimeField(db_column='updated on')  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Tokens'

from rest_framework import serializers
from .models import Project, HelpdeskUser, Member

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HelpdeskUser
        fields = '__all__'

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'is_public' ]


# TODO check on how to use relationships between multiple serializers
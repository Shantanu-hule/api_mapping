from rest_framework import serializers
from .models import Project_team, Type_color, Master
from .models import version
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_team
        fields = '__all__'



class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = '__all__'

class TypeColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_color
        fields = '__all__'

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = version
        fields = '__all__'


from rest_framework import serializers

class RemoveMappingSerializer(serializers.Serializer):
    source = serializers.CharField()

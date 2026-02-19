from rest_framework import serializers
from projects_app.models import Project
from contact_app.models import ContactMessage

class ProjectSerializer(serializers.ModelSerializer):
    tech_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'description', 'tech_stack', 
                 'tech_list', 'github_link', 'live_demo_link', 'created_date', 'image']
    
    def get_tech_list(self, obj):
        return obj.get_tech_list()

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message', 'timestamp']
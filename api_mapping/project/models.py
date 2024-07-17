# project_manager/models.py

from django.db import models

class Project_team(models.Model):
    project_name = models.CharField(max_length=100)
    project_manager = models.CharField(max_length=100)
    mapping = models.TextField()


class Type_color(models.Model):
    type = models.CharField(max_length=100)
    color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.type} - {self.color}"
    


class Subtype(models.Model):
    type = models.ForeignKey(Type_color, on_delete=models.CASCADE)
    subtype = models.CharField(max_length=100)

    def __str__(self):
        return self.subtype

    
class API_Mapping(models.Model):
    project = models.ForeignKey(Project_team, related_name='apis', on_delete=models.CASCADE)
    api = models.CharField(max_length=100)
    mapping = models.TextField()



class Master(models.Model):
    source=models.CharField(max_length=100)
    source_type=models.CharField(max_length=100)
    source_subtype=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    destination_type=models.CharField(max_length=100)
    destination_subtype=models.CharField(max_length=100)
    flow_num=models.CharField(max_length=100)
    two_way=models.CharField(max_length=100)
    project_team = models.ForeignKey(Project_team, on_delete=models.CASCADE)


class version(models.Model):
    project_team = models.ForeignKey(Project_team, on_delete=models.CASCADE)
    version_name=models.CharField(max_length=100)
    version_timestamp=models.CharField(max_length=100)
    mapping=models.CharField(max_length=100)


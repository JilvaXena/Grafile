import uuid
from django.db import models

# Create your models here.
class Group(models.Model):
    group_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    group_name = models.TextField(null=False, unique=True)
    group_text = models.TextField(null=True)

    date_created = models.DateTimeField(editable=False, null=False, auto_now_add=True)

    def __str__(self):
        return self.group_name + '/' + self.group_text

class File(models.Model):
    file_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)

    group = models.ForeignKey(Group, null=True, editable=True, on_delete=models.SET_NULL)

    #TODO: user_created = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)
    date_created = models.DateTimeField(null=False, editable=False, auto_now_add=True)

    path = models.TextField(editable=True, null=False)

    def __str__(self):
        return self.path

class GroupFiles(models.Model):
    group = models.ForeignKey(Group, null=False, on_delete=models.CASCADE)
    file = models.ForeignKey(File, null=False, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'file'],
                name='unique_group_file'
            )
        ]

class ModFiles(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    index = models.IntegerField(editable=False, null=False)
    file_hash = models.TextField(null=False, editable=False)
    date_update = models.DateTimeField(auto_now_add=True, editable=False)
    #TODO: user_update = models.ForeignKey(User, editable=False, on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['file', 'index'],
                name='unique_file_mod'
            )
        ]
        ordering = ['file', 'index']
    
    def save(self, *args, **kwargs):
        if not self.index:
            last_index = ModFiles.objects.filter(file=self.file).aggregate(max_index=Max('index'))['max_index']
        if last_index is not None:
            self.index = last_index + 1
        else:
            self.index = 0
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"File:{self.file}/Index:{self.index}"
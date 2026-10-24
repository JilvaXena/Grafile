import uuid
from django.db import models
from django.conf import settings

# Create your models here.
class Group(models.Model):
    group_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    group_name = models.TextField(null=False, unique=True)
    group_text = models.TextField(null=True)

    date_created = models.DateTimeField(editable=False, null=False, auto_now_add=True)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        editable=False
    )

    def __str__(self):
        return self.group_name + '/' + self.group_text

class File(models.Model):
    file_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)

    file_name = models.TextField(null=False, editable=True)

    group = models.ForeignKey(Group, null=True, editable=True, on_delete=models.SET_NULL)

    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        editable=False
    )
    date_created = models.DateTimeField(null=False, editable=False, auto_now_add=True)

    path = models.TextField(editable=True, null=False)

    def __str__(self):
        return self.path

class ModFiles(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    index = models.IntegerField(editable=False, null=False)
    
    file_hash = models.TextField(null=False, editable=False)
    
    date_update = models.DateTimeField(auto_now_add=True, editable=False)
    user_update = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        editable=False
    )

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
            last_index = ModFiles.objects.filter(file=self.file).aggregate(max_index=models.Max('index'))['max_index']
            if last_index is not None:
                self.index = last_index + 1
            else:
                self.index = 0
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"File:{self.file}/Index:{self.index}"


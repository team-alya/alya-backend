from django.db import models

#Model of pictures saved in database
class DBPicture(models.Model):
    dbpicture_title = models.TextField(max_length=100, blank=True)
    dbpicture = models.ImageField()

    def __str__(self):
        return self.dbpicture_title

#Model of Instructions
class Instruction(models.Model):
    id = models.AutoField(primary_key=True)
    instruction_title = models.TextField(max_length=100)
    instruction_text = models.TextField(max_length=500)

    def __str__(self):
        return self.instruction_text
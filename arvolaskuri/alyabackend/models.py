from django.db import models

#Model of pictures saved in database
class DBPicture(models.Model):
    dbpicture_title = models.TextField(max_length=100, blank=True)
    dbpicture = models.ImageField()

    def __str__(self):
        return self.dbpicture

#Model of Instructions
class Instruction(models.Model):
    instuction_title = models.TextField(max_length=100)
    instruction_text = models.TextField(default="instruction", max_length=500)

    def __str__(self):
        return self.instruction_text
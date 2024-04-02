from django.db import models


#Model of Instructions
class Instruction(models.Model):
    instuction_title = models.TextField(max_length=100)
    instruction_text = models.TextField(default="instruction", max_length=500)

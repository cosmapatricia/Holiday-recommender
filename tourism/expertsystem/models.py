from django.db import models

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=500)
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    def __str__(self):
        return self.choice_text
		

class Result(models.Model):
	result_name = models.CharField(max_length=100)
	result_text = models.CharField(max_length=500)
	def __str__(self):
		return self.result_name
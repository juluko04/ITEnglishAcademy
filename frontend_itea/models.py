from django.db import models

class Courses(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price = models.IntegerField()
    unitys = models.CharField(max_length=1000)
    start_date = models.CharField(max_length=50, default="")
    end_date = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name

class Dates(models.Model):
    date_name = models.CharField(max_length=50)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    start_date = models.DateField(max_length=50)
    end_date = models.DateField(max_length=50)
    
    def __str__(self):
        return self.date_name
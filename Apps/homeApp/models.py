import pickle
from django.db import models
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split



# Create your models here.

class FileUpload(models.Model):
    cc_num = models.CharField(max_length=50,default=0)
    actual_file = models.FileField(upload_to ='uploads/')
    status = models.CharField(max_length=400,null=True)

    def __str__(self):
        return self.cc_num
    
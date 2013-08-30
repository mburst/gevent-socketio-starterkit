from django.db import models
from django.contrib.auth.models import User
from django import forms

class Taco(models.Model):
    user = models.ForeignKey(User)
    status = models.CharField(max_length=155)
    
class TacoForm(forms.ModelForm):
    
    class Meta:
        model = Taco
        fields = ("status",)
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TacoForm, self).__init__(*args, **kwargs)
        
    def save(self):
        taco = super(TacoForm, self).save(commit=False)
        taco.user = self.user
        taco.save()
        return taco
    
    
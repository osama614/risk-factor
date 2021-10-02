from django.shortcuts import render
from rest_framework.generics import GenericAPIView
# Create your views here.

class Diagnose(GenericAPIView):
    total_rating = 29.73
    dignostic_data = {
        "age":{
            "<60": 0,
            "60-69": 2.3,
            "70-79": 3.72,
            ">80":6.13
            },
        "gender": {
            "male":1.85,
            "female":0
        },
        "race": {
            "asian":2.04,
            "black":1.33,
            "white":0,
            "hispanic": 1.22,
            "native AM Alaskan": 1.16,
            "pacific Islander":1.69
        },
        "smoking": {
            "yes":1.09,
            "no": 0
        },
        "BMI": {
            "<25": 0,
            "25-29":.99,
            "30-39":1.12,
            ">40":1.77
        },
        "exercise_level":{
            "high":0,
            "meduim":1.89,
            "low":2.26
        },
        "chronic_disease":{
            "organ_transplant":2.78,
            "pregnancy":4.16,
            "cardiovascular_disease":1.15,
            "COPD":1.16,
            "renal_disease":1.32,
            "cancer":1.23,
            "hypertension":1.14,
            "diabetes":1.65
    }
        
    }

    def get(self, request):
        data = request.data
        n = 0
        for i in data:
          n += self.dignostic_data[i][data[i]]

        #chronic_diseases = request.user.chronic_disease
        user_chronic_diseases = request.user.chronic_disease
        #user_chronic_diseases = chronic_diseases.filter()

        for k,v in self.dignostic_data["chronic_disease"]:
            
            if user_chronic_diseases.k:




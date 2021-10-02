from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
import math
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
    }

    loss_of_smell = 0
    fever         = 0
    covid_at_home = 0
    shortness_of_breath = 0
    myalgia             = 0
    cough               = 0
    nausea              = 0
    gender              = 0
    sore_throat         = 0
    coryza              = 0
    diarrhea            = 0

    def get(self, request):
        diagnostic_base_data =  {
            "loss_of_smell": self.loss_of_smell,
            "fever": self.fever,
            "covid_at_home": self.covid_at_home,
            "shortness_of_breath": self.shortness_of_breath,
            "myalgia": self.myalgia,
            "cough": self.cough,
            "nausea": self.nausea,
            "gender": self.gender,
            "sore_throat": self.sore_throat,
            "coryza": self.coryza,
            "diarrhea": self.diarrhea,
        }
        hospitability_data = request.data.get('hospitability')
        diagnostic_data = request.data.get('diagnostic')
        n = 0
        for i in hospitability_data:
          n += self.dignostic_data[i][hospitability_data[i]]

        if request.user.gender == 'male':
              diagnostic_base_data["gender"] = 1
              n += 1.85
        
        if  69 > request.user.age > 60 :
            n += 2.3
        elif 79 > request.user.age >= 70 :
            n += 3.72
        elif  request.user.age >= 80 : 
            n += 6.13

        user_chronic_diseases = request.user.chronic_diseases.all()
        if len(user_chronic_diseases) > 0:
            for j in user_chronic_diseases:
                n += float(j.severity) 
        print(f"this is n {n}")
        hospitability_factor = (n / self.total_rating) * (100) 
        hospitability_level = ""
        if 33.33 > hospitability_factor:
             hospitability_level = "low"
        if 100 > hospitability_factor>= 67:
             hospitability_level = "high"
        if 67 > hospitability_factor >= 33.33:
             hospitability_level = "medium"

        if len(diagnostic_data) > 0:
            for g in diagnostic_data:
                diagnostic_base_data[g] = diagnostic_data[g]

        

        prediction = (- 1.078) + (1.309 * diagnostic_base_data.get('loss_of_smell')) + (0.481 * diagnostic_base_data.get('fever')) + (0.407 * diagnostic_base_data.get('covid_at_home')) + (0.338 * diagnostic_base_data.get('shortness_of_breath')) + (0.237 * diagnostic_base_data.get('myalgia')) + (0.153 * diagnostic_base_data.get('cough')) + (0.035 * diagnostic_base_data.get('nausea')) + (0.033 * diagnostic_base_data.get('gender')) + (0.008 * request.user.age) - (0.441 * diagnostic_base_data.get('sore_throat')) - (0.227 * diagnostic_base_data.get('coryza')) - (0.045 * diagnostic_base_data.get('diarrhea'))
        probability_of_testing_positive = math.exp(prediction) /(1 + math.exp(prediction))

        return Response(
            {
            "hospitability":{
                "hospitability_factor":hospitability_factor,
                "hospitability_level" : hospitability_level
            },
            "Probability_of_testing_positive": probability_of_testing_positive * 100
        },
        status=status.HTTP_200_OK)

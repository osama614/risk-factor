from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
import math
# Create your views here.

class Diagnose(GenericAPIView):
    total_rating = 51.68
    risk_factor_cal = {
        "age":{
            "18-29": .56,
            "30-49": 0.6,
            "50-64": 1,
            ">=65":1.6
            },
        "gender": {
            "male":1.22,
            "female":1
        },
        "race": {
            "admixed_african_european":1.57,
            "european":1,
            "admixed_amerindian":1.11,
            "other": 0.95,
        },
    
        "BMI": {
            "30-35":1.19,
            "35-40":1.13,
            ">=40":1.59
        },
        "exposure":{

            "any":0.81,
            "biological_relative_tested_positive":1.16,
            "directly_exposed_to_someone_who_tested_positive":0.68,
            "healthcare_worker_directly_exposed":0.63,
            "household_member_tested_positive":0.88
        },
        "diagnostic":{
            "loss_of_smell": .89,
            "fever": 3.49,
            "covid_at_home": 0,
            "shortness_of_breath": 1,
            "myalgia": 1.44,
            "cough": 2.49,
            "nausea": 2.41,
            "sore_throat":1.11 ,
            "coryza":0 ,
            "diarrhea": 2.23,
            "headache": 1.05,
            }
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
        hospitability_data = request.data.get('risk_calculation')
        diagnostic_data = request.data.get('diagnostic')
        n = 1 # default female
        if hospitability_data:

            for i in hospitability_data:
                if i == "exposure":
                    for k in hospitability_data[i]:
                         n += self.risk_factor_cal[i][k]
                if i == "BMI":
                    h = hospitability_data["BMI"]["hight"]
                    w = hospitability_data["BMI"]["weight"]
                    bmi = w / (h*h)
                    if 35 > bmi >= 30:
                        n += self.risk_factor_cal[i]["30-35"]
                    elif 40 > bmi >= 35:
                        n += self.risk_factor_cal[i]["35-40"]
                    elif bmi >= 40:
                        n += self.risk_factor_cal[i][">=40"]
                if i == 'race':
                    n += self.risk_factor_cal[i][hospitability_data[i]]
        else:
            return Response({"message":"check your risk_calculation data!","error":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.gender == 'male':
              diagnostic_base_data["gender"] = 1
              n += .85 # female + .85 = male
        
        if  29 >= request.user.age > 18 :
            n += self.risk_factor_cal["age"]["18-29"]

        elif 49 >= request.user.age >= 30 :
            n += self.risk_factor_cal["age"]["30-49"]
        elif 64 >= request.user.age >= 50 :
            n += self.risk_factor_cal["age"]["50-64"]
        elif  request.user.age >= 65 : 
            n += self.risk_factor_cal["age"][">=65"]

        user_chronic_diseases = request.user.chronic_diseases.all()
        if len(user_chronic_diseases) > 0:
            for j in user_chronic_diseases:
                n += float(j.severity) 
        print(f"this is n {n}")
        

        if diagnostic_data:
            for g in diagnostic_data:
                if g != "headache":
                    diagnostic_base_data[g] = diagnostic_data[g]
                    n += self.risk_factor_cal["diagnostic"][g]
        else:
            return Response({"message":"check your diagnostic data!","error":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

        hospitability_factor = (n / self.total_rating) * (100) 
        hospitability_level = ""
        if 33.33 > hospitability_factor:
             hospitability_level = "low"
        if 100 > hospitability_factor>= 67:
             hospitability_level = "high"
        if 67 > hospitability_factor >= 33.33:
             hospitability_level = "medium"

        prediction = (- 1.078) + (1.309 * diagnostic_base_data.get('loss_of_smell')) + (0.481 * diagnostic_base_data.get('fever')) + (0.407 * diagnostic_base_data.get('covid_at_home')) + (0.338 * diagnostic_base_data.get('shortness_of_breath')) + (0.237 * diagnostic_base_data.get('myalgia')) + (0.153 * diagnostic_base_data.get('cough')) + (0.035 * diagnostic_base_data.get('nausea')) + (0.033 * diagnostic_base_data.get('gender')) + (0.008 * request.user.age) - (0.441 * diagnostic_base_data.get('sore_throat')) - (0.227 * diagnostic_base_data.get('coryza')) - (0.045 * diagnostic_base_data.get('diarrhea'))
        probability_of_testing_positive = math.exp(prediction) /(1 + math.exp(prediction))

        return Response(
            {
            "risk_factor":{
                "risk_factor_probability":hospitability_factor,
                "risk_factor_level" : hospitability_level
            },
            "probability_of_testing_positive": probability_of_testing_positive * 100
        },
        status=status.HTTP_200_OK)

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import User_profile

class User_Serializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        #username is phone number?
        fields = ['id','username', 'password']

class User_profile_Serializer(serializers.ModelSerializer):
    class Meta(object):
        model = User_profile
        fields = ['name','gender', 'seeking_gender','self_introduction',
                  'partner_expectation','location_longitude','location_latitude',
                  ]

    def create(self,validated_data):
        longitude = validated_data["location_longitude"]
        latitude = validated_data["location_latitude"]

        bucket = 1

        validated_data["location_bucket"] = bucket

        instance = User_profile(**validated_data)
        instance.save()

        return instance
    
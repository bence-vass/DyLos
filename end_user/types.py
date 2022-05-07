import graphene
from graphene_django import DjangoObjectType
from . import models


class EndUserType(DjangoObjectType):
    class Meta:
        model = models.EndUser


class PreferenceType(DjangoObjectType):
    class Meta:
        model = models.Preference


class HistoryType(DjangoObjectType):
    class Meta:
        model = models.History

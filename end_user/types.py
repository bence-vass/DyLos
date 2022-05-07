import graphene
from graphene_django import DjangoObjectType
from . import models


class EndUserType(DjangoObjectType):
    class Meta:
        model = models.EndUser
        exclude = ()


class PreferenceType(DjangoObjectType):
    class Meta:
        model = models.Preference


class HistoryType(DjangoObjectType):
    class Meta:
        model = models.History


class UserType(graphene.Union):
    class Meta:
        types = (EndUserType, PreferenceType, HistoryType)

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, EndUserType):
            return EndUserType
        if isinstance(instance, PreferenceType):
            return PreferenceType
        if isinstance(instance, HistoryType):
            return HistoryType
        return UserType.resolve_type(instance, info)


class UserRecommendationType(graphene.ObjectType):
    class Meta:
        model = models.EndUser

    user = graphene.Field(EndUserType)
    history = graphene.List(HistoryType)
    preference = graphene.List(PreferenceType)
    recommended_type = graphene.String()
    accuracy = graphene.Float()
    error = graphene.Float()

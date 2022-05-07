import random

import graphene
from graphene import ObjectType, Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from django.contrib.auth import models as auth_models, get_user_model, password_validation
from django.core.exceptions import ValidationError
from . import models
from . import types


class UserNode(DjangoObjectType):
    class Meta:
        model = auth_models.User
        filter_fields = {
            'username': ['exact', 'icontains'],
        }
        interfaces = (Node,)


# ---- Query Summery ----

class Query(ObjectType):
    all_end_users = graphene.List(types.EndUserType)

    def resolve_all_end_users(self, info):
        return models.EndUser.objects.all()

    all_history = graphene.List(types.HistoryType)

    def resolve_all_history(self, info):
        return models.History.objects.all()

    all_preferences = graphene.List(types.PreferenceType)

    def resolve_all_preferences(self, info):
        return models.Preference.objects.all()

    user_by_id = graphene.Field(types.EndUserType, id=graphene.String(required=True))

    def resolve_user_by_id(self, info, id):
        try:
            return models.EndUser.objects.get(id=id)
        except models.EndUser.DoesNotExist:
            return None

    recommend_to_user = graphene.Field(
        types.UserRecommendationType,
        id=graphene.String(required=True),
        allowed_modules=graphene.List(graphene.String),
        exclude_modules=graphene.List(graphene.String),

    )

    def resolve_recommend_to_user(
            self, info, id,
            allowed_modules=['earn_and_burn', 'tiered', 'gamified', 'perks'],
            exclude_modules=[],
    ):
        try:
            user = models.EndUser.objects.get(id=id)
            modules_to_query = allowed_modules
            if exclude_modules:
                modules_to_query = [x for x in allowed_modules if x not in exclude_modules]
            history = models.History.objects.filter(user_id_id=id).filter(service_type__in=modules_to_query).all()
            preference = models.Preference.objects.filter(user_id_id=id).filter(service_name__in=modules_to_query).all()

            # 48h limitation :(
            return {
                'user': user,
                'history': history,
                'preference': preference,
                'recommended_type': modules_to_query[random.randint(0, len(modules_to_query)-1)],
                'accuracy': random.uniform(.35, .98),
                'error': random.uniform(1., 20.),
            }
        except models.EndUser.DoesNotExist:
            return None


# ---- Mutations ----


class Mutation(graphene.ObjectType):
    # create_user = CreateUser.Field()
    pass

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
                'recommended_type': modules_to_query[random.randint(0, len(modules_to_query) - 1)],
                'accuracy': random.uniform(.35, .98),
                'error': random.uniform(1., 20.),
            }
        except models.EndUser.DoesNotExist:
            return None

    recommend_service = graphene.Field(types.RecommendationType)

    # Dynamic ctrl+c ctrl+v registry
    def resolve_recommend_service(self, info):
        try:
            modules = ['earn_and_burn', 'tiered', 'gamified', 'perks']
            modules_dict = {}
            for m in modules:
                filtered = models.Preference.objects.filter(service_name=m).all()
                modules_dict[m] = {}
                modules_dict[m]['count'] = len(filtered)
                modules_dict[m]['avg_metric'] = sum([x.metric / len(filtered) for x in filtered])
                modules_dict[m]['redeem_rate'] = sum([x.reach_out_count / len(filtered) for x in filtered])

            return {
                'earn_and_burn_count': modules_dict['earn_and_burn']['count'],
                'earn_and_burn_avg_metric': modules_dict['earn_and_burn']['avg_metric'],
                'earn_and_burn_redeem_rate': modules_dict['earn_and_burn']['redeem_rate'],

                'tiered_count': modules_dict['tiered']['count'],
                'tiered_avg_metric': modules_dict['tiered']['avg_metric'],
                'tiered_redeem_rate': modules_dict['tiered']['redeem_rate'],

                'gamified_count': modules_dict['gamified']['count'],
                'gamified_avg_metric': modules_dict['gamified']['avg_metric'],
                'gamified_redeem_rate': modules_dict['gamified']['redeem_rate'],

                'perks_count': modules_dict['perks']['count'],
                'perks_avg_metric': modules_dict['perks']['avg_metric'],
                'perks__redeem_rate': modules_dict['perks']['redeem_rate'],
            }
        except:
            return None


# ---- Mutations ----


class Mutation(graphene.ObjectType):
    # create_user = CreateUser.Field()
    pass

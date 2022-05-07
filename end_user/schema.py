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
            user = models.EndUser.objects.get(id=id)

            prefs = models.Preference.objects.filter(user_id_id=id)
            #user.extend(prefs)
            print(prefs)

            # hist = models.History.objects.filter(user_id_id=id)
            # data.extend(hist)
            return user
        except models.EndUser.DoesNotExist:
            return None


# ---- Mutations ----


# class ProfileMutation(graphene.Mutation):
#     user = graphene.Field(types.UserType)
#
#     def mutate(self, info, first_name='', last_name='', email=''):
#         user = get_user_model().objects.get(pk=info.context.user.id)
#         if first_name is not None and user.first_name != first_name:
#             user.first_name = first_name
#         if last_name is not None and user.last_name != last_name:
#             user.last_name = last_name
#         if email != '' and user.email != email:
#             try:
#                 validators.validate_unique_email(email)
#             except ValidationError as err:
#                 raise Exception(err)
#             user.email = email
#         user.save()
#         return ProfileMutation(user=user)


class Mutation(graphene.ObjectType):
    # create_user = CreateUser.Field()
    pass

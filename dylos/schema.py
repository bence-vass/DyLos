import graphene
from graphene_django import DjangoObjectType




class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    # posts = graphene.List()


    def resolve_posts(self, info):
        pass

schema = graphene.Schema(query=Query)

import graphene
import end_user.schema


class Query(
    end_user.schema.Query,
    graphene.ObjectType
):
    pass


class Mutation(
    # end_user.schema.Mutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query)

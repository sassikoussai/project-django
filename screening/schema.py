import graphene
from graphene_django import DjangoObjectType
from .models import EdgeNode, APIRequestLog
from django.db.models import Avg
from graphql import GraphQLError

class EdgeNodeType(DjangoObjectType):
    class Meta:
        model = EdgeNode
        fields = "__all__"

class APIRequestLogType(DjangoObjectType):
    class Meta:
        model = APIRequestLog
        fields = "__all__"

class EdgeNodePerformanceType(graphene.ObjectType):
    node = graphene.Field(EdgeNodeType)
    avg_response_time = graphene.Float()
    total_requests = graphene.Int()

class Query(graphene.ObjectType):
    edge_nodes = graphene.List(EdgeNodeType)
    node_logs = graphene.List(APIRequestLogType, node_id=graphene.ID())
    node_performance = graphene.Field(EdgeNodePerformanceType, node_id=graphene.ID(required=True))

    def resolve_edge_nodes(self, info):
        return EdgeNode.objects.all()

    def resolve_node_logs(self, info, node_id=None):
        if node_id:
            return APIRequestLog.objects.filter(edge_node__id=node_id)
        return APIRequestLog.objects.all()

    def resolve_node_performance(self, info, node_id):
        try:
            node = EdgeNode.objects.get(pk=node_id)
        except EdgeNode.DoesNotExist:
            raise GraphQLError("EdgeNode not found.")
        logs = APIRequestLog.objects.filter(edge_node=node)
        avg_response = logs.aggregate(Avg('response_time_ms'))['response_time_ms__avg'] or 0
        total = logs.count()
        return EdgeNodePerformanceType(node=node, avg_response_time=avg_response, total_requests=total)


class RegisterEdgeNode(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        ip_address = graphene.String(required=True)
        latitude = graphene.Float(required=True)
        longitude = graphene.Float(required=True)
    
    edge_node = graphene.Field(EdgeNodeType)

    @classmethod
    def mutate(cls, root, info, name, ip_address, latitude, longitude):
        node = EdgeNode(
            name=name,
            ip_address=ip_address,
            latitude=latitude,
            longitude=longitude
        )
        node.save()
        return RegisterEdgeNode(edge_node=node)

class HealthCheckEdgeNode(graphene.Mutation):
    class Arguments:
        node_id = graphene.ID(required=True)
        status = graphene.String(required=True)

    edge_node = graphene.Field(EdgeNodeType)

    @classmethod
    def mutate(cls, root, info, node_id, status):
        try:
            node = EdgeNode.objects.get(pk=node_id)
        except EdgeNode.DoesNotExist:
            raise GraphQLError("EdgeNode not found.")
        node.status = status
        node.save()
        return HealthCheckEdgeNode(edge_node=node)

class Mutation(graphene.ObjectType):
    register_edge_node = RegisterEdgeNode.Field()
    health_check_edge_node = HealthCheckEdgeNode.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
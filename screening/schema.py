import graphene
from graphene_django import DjangoObjectType
from .models import EdgeNode, APIRequestLog
from django.db.models import Avg

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
        # List all edge nodes
        return EdgeNode.objects.all()

    def resolve_node_logs(self, info, node_id=None):
        # List logs for all nodes, or a specific node if node_id is given
        if node_id:
            return APIRequestLog.objects.filter(edge_node__id=node_id)
        return APIRequestLog.objects.all()

    def resolve_node_performance(self, info, node_id):
        # Aggregate performance metrics for a specific node
        node = EdgeNode.objects.get(pk=node_id)
        logs = APIRequestLog.objects.filter(edge_node=node)
        avg_response = logs.aggregate(Avg('response_time_ms'))['response_time_ms__avg'] or 0
        total = logs.count()
        return EdgeNodePerformanceType(node=node, avg_response_time=avg_response, total_requests=total)

# (Retain your previous mutations from earlier steps)
class Mutation(graphene.ObjectType):
    # ...register_edge_node and health_check...
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
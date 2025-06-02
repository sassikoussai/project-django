from django.test import TestCase, Client
from .models import EdgeNode, APIRequestLog
from django.core.exceptions import ValidationError

class GraphQLTestCase(TestCase):
    def setUp(self):
        EdgeNode.objects.create(
            name="Test Node",
            latitude=40,
            longitude=30,
            status="healthy",
            ip_address="127.0.0.1"
        )

    def test_edge_nodes_query(self):
        client = Client()
        response = client.post(
            "/graphql/",
            data={"query": """
                query {
                  edgeNodes {
                    name
                    latitude
                  }
                }
            """},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["data"]["edgeNodes"][0]["name"], "Test Node")

class EdgeNodeModelTest(TestCase):
    def test_create_edge_node_valid_coordinates(self):
        node = EdgeNode.objects.create(
            name="Test Node",
            latitude=40.0,
            longitude=30.0,
            status="healthy",
            ip_address="127.0.0.1"
        )
        self.assertEqual(node.name, "Test Node")
        self.assertEqual(node.latitude, 40.0)
        self.assertEqual(node.longitude, 30.0)
        self.assertEqual(node.status, "healthy")
        self.assertEqual(node.ip_address, "127.0.0.1")

    def test_create_edge_node_invalid_latitude(self):
        node = EdgeNode(
            name="Invalid Latitude Node",
            latitude=200.0,  # invalid
            longitude=30.0,
            status="healthy",
            ip_address="127.0.0.1"
        )
        with self.assertRaises(ValidationError):
            node.full_clean()

    def test_create_edge_node_invalid_longitude(self):
        node = EdgeNode(
            name="Invalid Longitude Node",
            latitude=40.0,
            longitude=200.0,  # invalid
            status="healthy",
            ip_address="127.0.0.1"
        )
        with self.assertRaises(ValidationError):
            node.full_clean()

class APIRequestLogModelTest(TestCase):
    def test_create_api_request_log(self):
        edge_node = EdgeNode.objects.create(
            name="Node For Log",
            latitude=0.0,
            longitude=0.0,
            status="healthy",
            ip_address="127.0.0.1"
        )
        log = APIRequestLog.objects.create(
            edge_node=edge_node,
            response_time_ms=123.4,
            latitude=0.0,
            longitude=0.0,
            status_code=201,
            client_ip="127.0.0.1"
        )
        self.assertEqual(log.edge_node, edge_node)
        self.assertEqual(log.status_code, 201)
        self.assertAlmostEqual(log.response_time_ms, 123.4)
        self.assertEqual(log.client_ip, "127.0.0.1")
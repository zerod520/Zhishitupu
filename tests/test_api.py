import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from pydantic import ValidationError
from backend.app.main import create_app
from backend.app.config import Settings

class SkeletonTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(create_app(Settings(_env_file=None, graph_backend='demo')))
        self.client.__enter__()
    def tearDown(self):
        self.client.__exit__(None, None, None)
    def test_frontend(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertIn('知识图谱', self.client.get('/').text)
        for path in ('/app.js', '/styles.css', '/docs', '/openapi.json'):
            self.assertEqual(self.client.get(path).status_code, 200)
    def test_health(self):
        data = self.client.get('/api/v1/health').json()
        self.assertEqual(data['status'], 'ok')
        self.assertFalse(data['database_checked'])
    def test_graph(self):
        data = self.client.get('/api/v1/knowledge-graph/snapshot').json()
        self.assertEqual(data['mode'], 'demo')
        self.assertTrue(data['read_only'])
        self.assertEqual(len(data['nodes']), 3)
        self.assertEqual(len(data['edges']), 2)
        small = self.client.get('/api/v1/knowledge-graph/snapshot?limit=1').json()
        self.assertEqual(len(small['nodes']), 1)
        self.assertEqual(small['edges'], [])
    def test_limits(self):
        for value in ('0', '201', 'abc'):
            self.assertEqual(self.client.get('/api/v1/knowledge-graph/snapshot?limit='+value).status_code, 422)
    def test_placeholders(self):
        for module in ('data-governance', 'model-governance'):
            data = self.client.get('/api/v1/'+module+'/status').json()
            self.assertEqual(data['module'], module)
            self.assertEqual(data['status'], 'placeholder')
            self.assertEqual(data['implemented'], [])
    def test_database_failure_does_not_fallback(self):
        settings = Settings(_env_file=None, graph_backend='neo4j', neo4j_password='test-only')
        with TestClient(create_app(settings)) as client:
            with patch.object(client.app.state.graph, 'snapshot', side_effect=RuntimeError('private secret')):
                with self.assertLogs('backend.app.modules.knowledge_graph', level='ERROR'):
                    response = client.get('/api/v1/knowledge-graph/snapshot')
                self.assertEqual(response.status_code, 503)
                self.assertNotIn('private secret', response.text)
    def test_invalid_configuration(self):
        for kwargs in ({'graph_backend':'invalid'}, {'graph_backend':'neo4j','neo4j_password':''}, {'port':0}):
            with self.assertRaises(ValidationError):
                Settings(_env_file=None, **kwargs)

if __name__ == '__main__':
    unittest.main()

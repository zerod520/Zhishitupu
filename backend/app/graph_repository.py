from typing import Protocol
from neo4j import GraphDatabase
from .schemas import GraphSnapshot, Node, Edge
from .config import Settings

class GraphRepository(Protocol):
    def snapshot(self, limit: int) -> GraphSnapshot: ...
    def close(self) -> None: ...

class DemoGraphRepository:
    def snapshot(self, limit: int) -> GraphSnapshot:
        nodes = [Node(id="demo-asset", name="演示管段", labels=["Asset"]),
                 Node(id="demo-corrosion", name="腐蚀损伤", labels=["Damage"]),
                 Node(id="demo-leak", name="泄漏", labels=["Failure"])]
        edges = [Edge(source="demo-asset", target="demo-corrosion", type="HAS_DAMAGE"),
                 Edge(source="demo-corrosion", target="demo-leak", type="MAY_CAUSE")]
        selected = nodes[:limit]
        ids = {n.id for n in selected}
        return GraphSnapshot(mode="demo", nodes=selected,
                             edges=[e for e in edges if e.source in ids and e.target in ids])
    def close(self):
        pass

class Neo4jGraphRepository:
    def __init__(self, settings: Settings):
        self.driver = GraphDatabase.driver(settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password), connection_timeout=5)
        self.database = settings.neo4j_database

    def snapshot(self, limit: int) -> GraphSnapshot:
        # One read transaction keeps the induced graph internally consistent.
        def read(tx):
            records = list(tx.run("MATCH (n) RETURN elementId(n) AS id, "
                "coalesce(n.name, n.title, elementId(n)) AS name, labels(n) AS labels "
                "ORDER BY elementId(n) LIMIT $limit", limit=limit))
            nodes = [Node(id=r["id"], name=str(r["name"]), labels=r["labels"]) for r in records]
            ids = [n.id for n in nodes]
            relationships = tx.run("MATCH (a)-[r]->(b) WHERE elementId(a) IN $ids "
                "AND elementId(b) IN $ids RETURN elementId(a) AS source, "
                "elementId(b) AS target, type(r) AS type LIMIT 1000", ids=ids)
            return GraphSnapshot(mode="neo4j", nodes=nodes,
                edges=[Edge(**dict(r)) for r in relationships])
        with self.driver.session(database=self.database, default_access_mode="READ") as session:
            return session.execute_read(read)

    def close(self):
        self.driver.close()

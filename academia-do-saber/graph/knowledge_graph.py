from neo4j import GraphDatabase
import os


driver = GraphDatabase.driver(
    os.getenv("GRAPH_URI"),
    auth=(os.getenv("GRAPH_USER"), os.getenv("GRAPH_PASSWORD")),
)


async def register_knowledge(user_id: str, knowledge_area: str, certification: str):
    with driver.session() as session:
        session.run(
            """
            MERGE (u:User {id:$user_id})

            MERGE (k:KnowledgeArea {
                name:$knowledge_area
            })

            MERGE (c:Certification {
                name:$certification
            })

            MERGE (u)-[:MASTERED]->(k)

            MERGE (u)-[:CERTIFIED_IN]->(c)
            """,
            {
                "user_id": user_id,
                "knowledge_area": knowledge_area,
                "certification": certification,
            },
        )
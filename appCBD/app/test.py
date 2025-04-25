from neomodel import config, db

config.DATABASE_URL = 'bolt://neo4j:neo4j-password@localhost:7687'

results, _ = db.cypher_query("RETURN 1")
print(results)
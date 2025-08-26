from rdflib import Graph

G = Graph()
G.parse("kg/ttl/ontology.ttl", format="turtle")
G.parse("kg/ttl/products.ttl", format="turtle")

Q = """
PREFIX : <http://example.org/onto#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?p ?name ?cat ?price ?rating ?count WHERE {
  ?p a :Product ;
     :name ?name ;
     :inCategory ?c .
  OPTIONAL { ?c a :Category . ?c :name ?cat . }
  OPTIONAL { ?p :price ?price . }
  OPTIONAL { ?p :rating ?rating . }
  OPTIONAL { ?p :reviewCount ?count . }
}
LIMIT 10
"""

for row in G.query(Q):
    print(row)

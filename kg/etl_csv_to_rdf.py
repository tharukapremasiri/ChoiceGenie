from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD
import csv, re

# Base namespace for your ontology
BASE = "http://example.org/onto#"
EX = Namespace(BASE)

# Helper: make safe URIs from names
def slugify(s: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]+', '-', s.strip()).lower()

# Create graph
g = Graph()
g.bind("ex", EX)

# Load ontology so schema (classes/properties) are included
g.parse("kg/ttl/ontology.ttl", format="turtle")

# Read CSV data
with open("data/raw/products.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pid = row["id"].strip()
        p_uri = URIRef(BASE + pid)

        # Add product type
        g.add((p_uri, RDF.type, EX.Product))

        # Add name, price, rating
        g.add((p_uri, EX.name, Literal(row["name"], datatype=XSD.string)))
        g.add((p_uri, EX.price, Literal(float(row["price"]), datatype=XSD.decimal)))
        g.add((p_uri, EX.rating, Literal(float(row["rating"]), datatype=XSD.decimal)))

        # Category handling
        cat = slugify(row["category"])
        c_uri = URIRef(BASE + cat)
        g.add((c_uri, RDF.type, EX.Category))
        g.add((p_uri, EX.inCategory, c_uri))

# Save to TTL
g.serialize("kg/ttl/products.ttl", format="turtle")
print("✅ RDF triples saved to kg/ttl/products.ttl")

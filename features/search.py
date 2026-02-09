from sqlalchemy import select, text
from app.db import SessionLocal
from sql.init_db import restaurants
from scripts.seed_db import get_embedding  # Reuse the embedding logic

def search_restaurants(query_text: str, limit: int = 5):
    """
    Semantic search for restaurants using pgvector.
    """
    # 1. Convert query text to vector
    query_vector = get_embedding(query_text)
    
    # 2. SQLAlchemy query with pgvector operator
    # <-> is the Euclidean distance operator (L2 distance)
    # <=> is Cosine distance (usually preferred for normalized embeddings)
    # <#> is Inner product
    
    # We use text() to wrap the operator if the type isn't fully recognized by SQLAlchemy's core
    # But since we defined the column as Vector384Type, we can use the op() method.
    
    session = SessionLocal()
    try:
        # Calculate distance
        distance_col = restaurants.c.embedding.op('<=>')(str(query_vector))
        
        stmt = (
            select(
                restaurants.c.id,
                restaurants.c.name,
                restaurants.c.description,
                restaurants.c.cuisine,
                distance_col.label("distance")
            )
            .order_by(distance_col)
            .limit(limit)
        )
        
        results = session.execute(stmt).all()
        
        return [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "cuisine": r.cuisine,
                "similarity": 1 - r.distance  # Convert distance to similarity score
            }
            for r in results
        ]
    finally:
        session.close()

if __name__ == "__main__":
    # Quick test
    results = search_restaurants("spicy asian food with noodles")
    for r in results:
        print(f"{r['name']} ({r['similarity']:.2f}): {r['description']}")
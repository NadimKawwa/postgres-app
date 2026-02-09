import sys 
import json 
import torch 
import torch.nn.functional as F 
from pathlib import Path 
from sqlalchemy import text 

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db import SessionLocal
from app.embedding import tokenizer, model
from sql.init_db import restaurants, reviews

def get_embedding(text_input):
    # Ensure input is a list
    if isinstance(text_input, str):
        text_input = [text_input]
        
    encoded_input = tokenizer(text_input, padding=True, truncation=True, return_tensors='pt')
    
    with torch.no_grad():
        model_output = model(**encoded_input)
        # Perform pooling. For BGE, use the first token (CLS)
        sentence_embeddings = model_output[0][:, 0]
        # Normalize embeddings
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
        
    return sentence_embeddings[0].tolist()


def seed():
    session = SessionLocal()
    try:
        # Load JSON data
        with open("raw_data/restaurants.json", "r") as f:
            rest_data = json.load(f)
        with open("raw_data/reviews.json", "r") as f:
            reviews_data = json.load(f)

        print(f"Found {len(rest_data)} restaurants and {len(reviews_data)} reviews.")

        # Clear existing data
        session.execute(text("TRUNCATE TABLE reviews, restaurants RESTART IDENTITY CASCADE"))
        
        # Insert Restaurants
        for r in rest_data:
            print(f"Processing {r['name']}...")
            # Generate embedding for description
            embedding = get_embedding(r['description'])
            
            # Prepare insert statement
            stmt = restaurants.insert().values(
                name=r['name'],
                address=r['address'],
                cuisine=r['cuisine'],
                hours=r['hours'],
                rating=r['rating'],
                review_count=r['review_count'],
                description=r['description'],
                embedding=embedding
            )
            session.execute(stmt)
        
        # Insert Reviews
        for rv in reviews_data:
            stmt = reviews.insert().values(
                restaurant_id=rv['restaurant_id'],
                text=rv['text'],
                rating=rv['rating']
            )
            session.execute(stmt)

        session.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    seed()
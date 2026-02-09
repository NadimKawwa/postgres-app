from postgrest import SyncPostgrestClient
from app.schemas import RestaurantCreate, RestaurantUpdate

#base URL 
PGRST_URL = "http://localhost:3005"

def get_client():
    return SyncPostgrestClient(PGRST_URL, schema='public')

#GET method
def list_restaurants(limit=10):
    client = get_client()
    return client.table('restaurants').select('*').limit(limit).execute()

def get_restaurant_by_id(pk: int):
    client = get_client()
    return client.table("restaurants").select("*").eq("id", pk).single().execute() 

# POST method 
def create_restaurant(data: dict):
    # Validate input
    validated_data = RestaurantCreate(**data)
    client = get_client()
    # dump_mode='json' ensures nested dicts like address are handled correctly
    return client.table("restaurants").insert(validated_data.model_dump(mode='json')).execute()

#PUT method 
def update_restaurant(pk: int, data: dict):
    # Validate input (partial update)
    validated_data = RestaurantUpdate(**data)
    # exclude_unset=True ensures we don't send None for missing fields
    payload = validated_data.model_dump(exclude_unset=True, mode='json')
    
    if not payload:
        return {"message": "No valid fields to update"}
        
    client = get_client()
    return client.table("restaurants").update(payload).eq("id", pk).execute()
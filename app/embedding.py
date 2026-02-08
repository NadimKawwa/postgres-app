import json 
import torch 

from transformers import AutoTokenizer, AutoModel


MODEL_ID = 'BAAI/bge-small-en-v1.5'
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModel.from_pretrained(MODEL_ID)



def load_data(restaurant_dir: str, reviews_dir: str):
    with open (restaurant_dir, 'r') as f:
        rest_dict = json.load(f)

    with open (reviews_dir, 'r') as f:
        reviews_dict = json.load(f)

    

    return rest_dict, reviews_dict



def main():
    rest_arr, reviews_arr = load_data("raw_data/restaurants.json", "raw_data/reviews.json")

    print(rest_arr[0])
    print(10*'-')
    print(reviews_arr[0])

    sentences = [rest['description'] for rest in rest_arr]
    print(sentences)

    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')


    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    print(f"model_output =\n {model_output}")

     


if __name__ == '__main__':
    main()
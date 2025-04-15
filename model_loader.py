# backend/core/model_loader.py

import os
from gpt4all import GPT4All

def load_model(model_path: str):
    """Loads the GPT4All model from the specified path."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"The model file at {model_path} was not found.")
    
    model = GPT4All(model_path)
    return model

def test_model(model):
    """Test the model by sending a basic prompt."""
    prompt = "Hello, how are you?"
    response = model.generate(prompt)
    print("Model Response:", response)

def main():
    """Main function to load and test the model."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    models_dir = os.path.join(base_dir, "models")
    model_file = "Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf"  # Update with the correct model file name
    model_path = os.path.join(models_dir, model_file)

    try:
        model = load_model(model_path)
        print("Model loaded successfully.")
        test_model(model)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

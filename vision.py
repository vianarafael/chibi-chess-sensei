from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch

# Japanese labels and explanations (text embeddings)
CANDIDATES = {
    "ルーク": "ルーク：おしろの形をした駒",
    "ビショップ": "ビショップ：とんがり帽子のような駒",
    "ナイト": "ナイト：馬の顔の形をした駒",
    "クイーン": "クイーン：きれいな冠をかぶった駒",
    "キング": "キング：大きな冠をかぶった駒",
    "ポーン": "ポーン：小さくてまるい頭の駒",
}

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def classify_piece(image: Image.Image) -> str:
    """
    Uses CLIP to classify a chess piece by comparing the image to Japanese-language descriptions.
    """
    # Convert label texts to list
    texts = list(CANDIDATES.values())
    labels = list(CANDIDATES.keys())

    # Preprocess inputs
    inputs = processor(text=texts, images=image, return_tensors="pt", padding=True)

    # Run model
    with torch.no_grad():
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)

    # Pick best match
    best_index = probs[0].argmax().item()
    predicted_label = labels[best_index]
    confidence = probs[0][best_index].item()

    print(f"[CLIP] Predicted: {predicted_label} ({confidence:.2f})")
    return predicted_label

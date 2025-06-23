from sentence_transformers import SentenceTransformer, util
import torch

class IntentClassifier:
    def __init__(self):
        # 1. Device setup
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print("🚀 Using device:", self.device)

        # 2. Load model
        self.model = SentenceTransformer("BAAI/bge-large-en-v1.5", device=self.device)

        # 3. Define intent map
        self.intent_map = {
            "Very Cold": [
                "I’m freezing", "It’s like Antarctica", "Why is it so icy?", "I can’t feel my fingers", "This is too cold to function"
            ],
            "Cold": [
                "It’s too cold", "Can we warm it up a bit?", "I’m a little chilly", "It feels cold here", "My hands are cold", "Its not hot here"
            ],
            "Comfortable": [
                "It’s perfect now", "Feels okay", "This is just right", "I’m comfortable", "No change needed"
            ],
            "Warm": [
                "It’s getting warm", "A bit toasty", "It’s a little warm in here", "Starting to sweat", "Warm but manageable", "Not cold here"
            ],
            "Hot": [
                "I’m sweating buckets", "It’s too hot", "Feels like a sauna", "Why is it so hot?", "I’m melting"
            ]
        }

        # 4. Preprocess and encode phrases
        self.intent_texts = []
        self.intent_labels = []

        for label, phrases in self.intent_map.items():
            for phrase in phrases:
                self.intent_texts.append(phrase)
                self.intent_labels.append(label)

        self.intent_embeddings = self.model.encode(self.intent_texts, convert_to_tensor=True, device=self.device)

    def classify_text(self, user_input):
        user_emb = self.model.encode(user_input, convert_to_tensor=True, device=self.device)
        scores = util.cos_sim(user_emb, self.intent_embeddings)
        best_idx = torch.argmax(scores).item()
        return self.intent_labels[best_idx]
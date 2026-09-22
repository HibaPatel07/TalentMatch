from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-en-v1.5"


class EmbeddingModel:
    def __init__(self, model_name=MODEL_NAME):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        """
        Generate embeddings for one or more texts.
        """
        if isinstance(texts, str):
            texts = [texts]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings


def load_embedding_model():
    """
    Load and return the pretrained BGE embedding model.
    """
    return EmbeddingModel()
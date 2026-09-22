import numpy as np


def cosine_similarity(embedding_1, embedding_2):
    """
    Calculate cosine similarity between two embeddings.
    """

    embedding_1 = np.asarray(embedding_1)
    embedding_2 = np.asarray(embedding_2)

    similarity = np.dot(embedding_1, embedding_2)

    return float(similarity)
    
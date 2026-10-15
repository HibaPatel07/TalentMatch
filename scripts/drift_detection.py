import numpy as np
from scipy.stats import ks_2samp
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def detect_embedding_drift(train_path, prod_path, p_value_threshold=0.05):
    """
    Compares training and production embedding distributions.
    Uses the Kolmogorov-Smirnov (KS) test to detect statistical drift.
    """
    logger.info("Loading embeddings...")
    # Replace these with your actual data loading logic (e.g., np.load)
    # train_embeddings = np.load(train_path)
    # prod_embeddings = np.load(prod_path)
    
    # Simulating data for testing the pipeline
    np.random.seed(42)
    train_embeddings = np.random.normal(0, 1, 1000) 
    prod_embeddings = np.random.normal(0.2, 1.2, 1000) # Simulated shift in production data

    logger.info("Running statistical comparison...")
    # Flatten embeddings if they are multi-dimensional before running KS test
    stat, p_value = ks_2samp(train_embeddings.flatten(), prod_embeddings.flatten())
    
    logger.info(f"Drift Score (p-value): {p_value:.5f}")
    
    if p_value < p_value_threshold:
        logger.warning("🚨 DRIFT DETECTED! Production data distribution has shifted.")
        return True
    else:
        logger.info("✅ Data is stable. No drift detected.")
        return False

if __name__ == "__main__":
    # Example paths
    drift_flag = detect_embedding_drift("data/train_emb.npy", "data/prod_emb.npy")
    
    if drift_flag:
        logger.info("Action: Triggering retraining workflow...")
        # Later, we can have this trigger your Airflow retraining DAG
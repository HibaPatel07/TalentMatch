# syntax=docker/dockerfile:1
# ---------- TalentMatch inference API (FastAPI + Sentence-Transformers) ----------
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/opt/hf-cache \
    PORT=8000

# Run as a non-root user (security best practice)
RUN useradd --create-home --uid 1000 appuser
WORKDIR /app

# 1) Dependencies first -> this layer is cached until requirements change.
#    CPU-only PyTorch keeps the image ~1 GB smaller than the default CUDA build.
COPY requirements-api.txt .
RUN pip install --index-url https://download.pytorch.org/whl/cpu torch \
 && pip install -r requirements-api.txt

# 2) Bake the embedding model into the image so the container starts offline
#    and does not download from Hugging Face on every start.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-en-v1.5')" \
 && chown -R appuser:appuser /opt/hf-cache

# 3) Application code last (changes most often).
COPY --chown=appuser:appuser api.py .
COPY --chown=appuser:appuser src ./src
COPY --chown=appuser:appuser frontend ./frontend

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status==200 else 1)"

CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT}"]

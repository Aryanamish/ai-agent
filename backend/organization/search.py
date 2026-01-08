import numpy as np
import os
from django.conf import settings
from .models import Products
from aichatbot.utils import set_organization_slug, clear_organization_slug

# Try imports
try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
except ImportError:
    GoogleGenerativeAIEmbeddings = None

def get_embedding_model():
    api_key = os.environ.get("GOOGLE_API_KEY") or getattr(settings, "GOOGLE_API_KEY", None)
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not set.")
    return GoogleGenerativeAIEmbeddings(google_api_key=api_key, model="models/embedding-001")

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def search_products(query: str, org_slug: str, top_k: int = 5):
    """
    Search for products in a specific organization using semantic search.
    
    Args:
        query: User's search query (strings).
        org_slug: The slug of the organization database to search in.
        top_k: Number of results to return.
        
    Returns:
        List of dictionaries containing product details and similarity score.
    """
    # 1. Embed Query
    from llm.llm import LLM
    try:
        llm_instance = LLM(provider="ollama")
        model = llm_instance.get_embedding_model()
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        return []

    query_vector = model.embed_query(query)
    
    # 2. Fetch Products
    # We must set the context to the correct org DB
    # We use a context manager or try/finally block
    # But since we are likely calling this from verified context or needing to switch:
    
    previous_slug = settings.DATABASES.get('default').get('NAME') # Just a placeholder check or use utils
    # Actually, we should use the router logic via utils
    
    # Actually, we should use the router logic via utils
    
    # We set it for this search operation. 
    # Since we removed the finally/clear, this is now "switch scope".
    # This relies on the caller (View) to clean up or the thread to die.
    set_organization_slug(org_slug)
    
    # Ensure DB exists in settings (dynamic add if needed - reusing logic from router/signals)
    if org_slug not in settings.DATABASES:
         new_db = settings.DATABASES['default'].copy()
         new_db['NAME'] = settings.BASE_DIR / f"db/{org_slug}.sqlite3"
         settings.DATABASES[org_slug] = new_db

    try:
        products = Products.objects.exclude(embedding__isnull=True)
        # Note: If database is large, fetching all embeddings to memory is bad.
        # But for <10k it's perfectly fine and fast.
        
        results = []
        for product in products:
            if not product.embedding:
                continue
            
            # DB returns JSONList, usually python list. Convert to numpy.
            prod_vector = np.array(product.embedding)
            score = cosine_similarity(query_vector, prod_vector)
            
            results.append({
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "attributes": product.attributes,
                "image": product.image if product.image else None,
                "score": float(score)
            })
            
        # 3. Sort and Return
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
        
    # 3. Sort and Return
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
        
    finally:
        # We should NOT blindly clear it if we are in a larger request context.
        # However, for safety in standalone scripts, we want to clear.
        # But in a nested call stack like View -> Node -> Search, clearing breaks the View.
        # Ideally, we check if we changed it.
        # For this codebase, let's REMOVE the clear and let the View/Middleware handle it.
        # OR better: restore previous.
        pass
        # clear_organization_slug() # CAUSING BUG IN CHAT VIEW

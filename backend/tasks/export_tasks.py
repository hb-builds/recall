from celery import shared_task
from extensions import cache
from services.export_service import generate_attempts_csv, generate_all_quizzes_csv

@shared_task(bind=True)
def generate_user_attempts_csv(self, user_id: int):
    """
    Celery task to generate CSV and store the download path in cache.
    """
    filepath = generate_attempts_csv(user_id)
    # Cache the filepath for retrieval (e.g., 1 hour expiry)
    cache_key = f"export_user_{user_id}_{self.request.id}"
    cache.set(cache_key, filepath, timeout=3600)
    return {'filepath': filepath}

@shared_task(bind=True)
def generate_admin_quizzes_csv(self):
    """
    Celery task to generate CSV of all quizzes and store the download path in cache.
    """
    filepath = generate_all_quizzes_csv()
    cache_key = f"export_admin_quizzes_{self.request.id}"
    cache.set(cache_key, filepath, timeout=3600)
    return {'filepath': filepath}

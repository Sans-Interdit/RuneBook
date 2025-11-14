from data.models import Event, session, User
from sqlalchemy import func
import cloudinary
import cloudinary.api
import cloudinary.uploader
import re
import os

cloudinary.config(  
    cloud_name = "da2qstwtv",
    api_key = os.getenv("CLOUDINARY_API_KEY"), 
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def cleanup_old_events():
    past_events = session.query(Event).filter(Event.end_time < func.now()).all()
    for event in past_events:
        session.delete(event)
    
    session.commit()
    session.close()

# Fonction utilitaire pour récupérer toutes les ressources Cloudinary
def get_all_resources():
    all_resources = []
    response = cloudinary.api.resources(max_results=500)
    all_resources.extend(response["resources"])
    while "next_cursor" in response:
        response = cloudinary.api.resources(max_results=500, next_cursor=response["next_cursor"])
        all_resources.extend(response["resources"])
    return all_resources

def extract_public_id(url):
    # Exemple d'URL : .../upload/c_fill,f_auto/.../v1234567890/public_id.png
    match = re.search(r"/v\d+/(.+)\.\w+$", url)
    return match.group(1) if match else None


def cleanup_old_images():
    # Récupérer toutes les URLs stockées dans la BDD
    photos = session.query(Event.photo).all()
    photos = [p[0] for p in photos if p[0] is not None]
    
    db_public_ids = [extract_public_id(url) for url in photos if extract_public_id(url)]

    # Récupération de toutes les ressources
    resources = get_all_resources()

    for res in resources:
        public_id = res["public_id"]

        # Si le public_id n'est pas en BDD => supprimer
        if public_id not in db_public_ids:
            print(f"Suppression de {public_id}")
            cloudinary.uploader.destroy(public_id)


if __name__ == "__main__":
    cleanup_old_events()
    cleanup_old_images()

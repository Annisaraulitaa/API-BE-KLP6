from src.services.firebase import storage

# function to delete image from firebase storage link
import firebase_admin
from firebase_admin import storage

def delete_image_from_firebase(path: str):
    try:
        # Process the URL to get the path
        path = path.split('https://firebasestorage.googleapis.com/v0/b/')[1]
        path = path.split('%2F')[1]
        path = path.split('?alt')[0]
        
        # Get a reference to the image blob
        blob = storage.bucket().blob(path)
        
        # Check if the blob exists before attempting to delete
        if blob.exists():
            # Delete the blob
            blob.delete()
            return True, 'success'
        else:
            return False, 'Image not found'
    except Exception as e:
        return False, str(e)

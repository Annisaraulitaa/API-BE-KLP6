from src.services.firebase import storage

# function to delete image from firebase storage link
from firebase_admin import storage

def delete_image_from_firebase(url: str):
    try:
        # Check if the URL matches the expected format
        if not url.startswith('https://storage.googleapis.com/'):
            return False, 'Invalid URL format'

        # Process the URL to get the path
        path = url.split('https://storage.googleapis.com/')[1]

        # The path might include the bucket name, so we need to remove it
        path = '/'.join(path.split('/')[1:])

        # Print the path for debugging
        print(f"Blob path: {path}")

        # Get a reference to the image blob
        blob = storage.bucket().blob(path)

        # Check if the blob exists before attempting to delete
        if blob.exists():
            # Delete the blob
            blob.delete()
            return True, 'Success'
        else:
            return False, 'Image not found'
    except Exception as e:
        return False, str(e)

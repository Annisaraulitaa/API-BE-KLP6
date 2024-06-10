import os
from typing import Optional
from src.services.firebase import storage

def upload_image_to_firebase(file, file_name: Optional[str] = None, allowed: Optional[set] = None):
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    
    if allowed:
        allowed_extensions = allowed
        
    if file:
        # Periksa ekstensi file
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        if file_extension not in allowed_extensions:
            return None, 'Invalid file type'
        # Simpan file ke temp
        file_path = '/tmp/' + file.filename
        file.save(file_path)

        # Upload file ke Firebase Storage
        blob = storage.blob(file.filename if not file_name else f'{file_name}.{file_extension}')
        blob.upload_from_filename(file_path)

        # Hapus file sementara dari temp
        os.remove(file_path)

        # Dapatkan URL publik untuk file yang diunggah
        url = blob.public_url

        return url, 'success'

    return None, 'No file provided'
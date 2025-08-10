import os
import uuid
from PIL import Image
from fastapi import UploadFile
import aiofiles
from app.core.config import settings

async def save_upload_file(upload_file: UploadFile) -> str:
    """
    Save an uploaded file to the uploads directory
    
    Args:
        upload_file: The uploaded file
        
    Returns:
        The path to the saved file
    """
    # Create uploads directory if it doesn't exist
    os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
    
    # Generate a unique filename
    file_extension = os.path.splitext(upload_file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_FOLDER, unique_filename)
    
    # Save the file
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await upload_file.read()
        await out_file.write(content)
    
    return file_path

async def clip_image(image_path: str, x: int, y: int, width: int, height: int) -> str:
    """
    Clip an image to the specified dimensions
    
    Args:
        image_path: Path to the image
        x: X coordinate of the top-left corner
        y: Y coordinate of the top-left corner
        width: Width of the clipped area
        height: Height of the clipped area
        
    Returns:
        The path to the clipped image
    """
    # Open the image
    img = Image.open(image_path)
    
    # Clip the image
    clipped_img = img.crop((x, y, x + width, y + height))
    
    # Generate a new filename for the clipped image
    file_name, file_extension = os.path.splitext(image_path)
    clipped_image_path = f"{file_name}_clipped{file_extension}"
    
    # Save the clipped image
    clipped_img.save(clipped_image_path)
    
    return clipped_image_path

def is_allowed_file(filename: str) -> bool:
    """
    Check if a file has an allowed extension
    
    Args:
        filename: The filename to check
        
    Returns:
        True if the file has an allowed extension, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS
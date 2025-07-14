from boxsdk import JWTAuth, Client

# Authenticate with Box
auth = JWTAuth.from_settings_file("231434_01yj1fya_config.json")
client = Client(auth)

# Define media file extensions
image_extensions = {".jpg", ".jpeg"}
video_extensions = {".mp4", ".mov", ".avi", ".mkv", ".wmv"}

# Global counters
total_image_count = 0
total_video_count = 0

# Function to get folder ID by name
def get_folder_id_by_name(parent_folder_id, target_folder_name):
    items = list(client.folder(folder_id=parent_folder_id).get_items(limit=1000))
    for item in items:
        if item.type == "folder" and item.name.lower() == target_folder_name.lower():
            return item.id
    return None

# Function to check if a file is a media file
def is_media_file(file_name):
    file_name = file_name.lower()
    return any(file_name.endswith(ext) for ext in image_extensions | video_extensions)

# Function to search for media files inside the "movie" folder and its subfolders
def search_for_media(folder_id, folder_name):
    global total_image_count, total_video_count
    print(f"Processing 'movie' folder: {folder_name}")  # Print which folder is being processed
    items = list(client.folder(folder_id=folder_id).get_items(limit=1000))
    print(f"Total video files found inside 'movie': {total_video_count}")
    for item in items:
        if item.type == "file":
            if any(item.name.lower().endswith(ext) for ext in image_extensions):
                total_image_count += 1
            elif any(item.name.lower().endswith(ext) for ext in video_extensions):
                total_video_count += 1
        elif item.type == "folder":
            search_for_media(item.id, item.name)  # Recursively go deeper into subfolders

# Get the "movie" folder inside root
root_folder_id = "3954670807"
movie_folder_id = get_folder_id_by_name(root_folder_id, "movie")

# If the movie folder exists, search inside it
if movie_folder_id:
    search_for_media(movie_folder_id, "movie")
    print(f"\nTotal image files found inside 'movie': {total_image_count}")
    print(f"Total video files found inside 'movie': {total_video_count}")
else:
    print("Movie folder not found in root")

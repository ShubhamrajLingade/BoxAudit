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

def get_folder_id_by_name(parent_folder_id, target_folder_name):
    """Returns the folder ID of a given folder name inside the parent folder."""
    items = list(client.folder(folder_id=parent_folder_id).get_items(limit=1000))
    for item in items:
        if item.type == "folder" and item.name.lower() == target_folder_name.lower():
            return item.id
    return None

def search_for_complete_folders(parent_folder_id, parent_folder_name):
    """Finds all folders containing 'complete' in their name and processes them."""
    items = list(client.folder(folder_id=parent_folder_id).get_items(limit=1000))

    print(f"Processing folder: {parent_folder_name}")  # Print the folder inside "old"
    print(f"Total image files found: {total_image_count}" f'Total video files found: {total_video_count}')

    for item in items:
        if item.type == "folder" and "complete" in item.name.lower():
            search_for_media(item.id)

def search_for_media(folder_id):
    """Recursively searches for media files inside a folder."""
    global total_image_count, total_video_count
    items = list(client.folder(folder_id=folder_id).get_items(limit=1000))

    for item in items:
        if item.type == "file":
            if any(item.name.lower().endswith(ext) for ext in image_extensions):
                total_image_count += 1
            elif any(item.name.lower().endswith(ext) for ext in video_extensions):
                total_video_count += 1
        elif item.type == "folder":
            search_for_media(item.id)  # Recursively process subfolders

def process_old_folders(root_folder_id):
    """Finds the 'old' folder and processes each subfolder inside it."""
    old_folder_id = get_folder_id_by_name(root_folder_id, "old")
    if not old_folder_id:
        print("Old folder not found in root")
        return

    old_subfolders = list(client.folder(folder_id=old_folder_id).get_items(limit=1000))
    for subfolder in old_subfolders:
        if subfolder.type == "folder":
            search_for_complete_folders(subfolder.id, subfolder.name)

# Main execution
root_folder_id = "3954670807"
process_old_folders(root_folder_id)

# Final output
print(f"\n Here Total image files found: {total_image_count}")
print(f"Here Total video files found: {total_video_count}")

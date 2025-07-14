import asyncio
import json
import os
from boxsdk import JWTAuth, Client

# Authentication
auth = JWTAuth.from_settings_file(r"231434_01yj1fya_config.json")
client = Client(auth)

user = client.user().get()
print(f"Authenticated as: {user.name}")

# File Extensions
image_extensions = {".jpg", ".jpeg"}
video_extensions = {".mp4", ".mov", ".avi", ".mkv", ".wmv"}

# Global Counters
total_image_count = 0
total_video_count = 0

# Checkpoint File
CHECKPOINT_FILE = "checkpoint.json"


def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            return json.load(f)
    return {"last_folder": None}


def save_checkpoint(folder_id):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({"last_folder": folder_id}, f)


async def get_folder_ids_by_name(parent_folder_id, target_folder_name):
    matching_folders = []
    items = await asyncio.to_thread(client.folder(folder_id=parent_folder_id).get_items)
    for item in items:
        if item.type == "folder" and item.name.lower() == target_folder_name.lower():
            matching_folders.append(item.id)
    return matching_folders


async def search_for_media(folder_id):
    global total_image_count, total_video_count
    items = await asyncio.to_thread(client.folder(folder_id=folder_id).get_items)

    for item in items:
        if item.type == "file":
            if any(item.name.lower().endswith(ext) for ext in image_extensions):
                total_image_count += 1
            elif any(item.name.lower().endswith(ext) for ext in video_extensions):
                total_video_count += 1
        elif item.type == "folder":
            await search_for_media(item.id)


async def search_photography_and_movies(complete_folder_id):
    for target_folder in ["photography", "movie"]:
        target_folder_ids = await get_folder_ids_by_name(complete_folder_id, target_folder)
        for folder_id in target_folder_ids:
            await search_for_media(folder_id)


async def search_complete_folders(order_folder_id):
    complete_folder_ids = await get_folder_ids_by_name(order_folder_id, "complete")
    for folder_id in complete_folder_ids:
        await search_photography_and_movies(folder_id)


async def process_assets_folders(assets_folder_id, resume_from=None):
    items = await asyncio.to_thread(client.folder(folder_id=assets_folder_id).get_items)
    global total_image_count, total_video_count

    start_processing = resume_from is None  # If no resume point, start immediately

    for item in items:
        if item.type == "folder":
            if not start_processing:
                if item.id == resume_from:                  start_processing = True  # Resume from this folder
                else:
                    continue  # Skip until we find the last processed folder

            print(f"Processing folder: {item.name}")  # Print only the folder name
            await search_complete_folders(item.id)

            save_checkpoint(item.id)  # Save progress

            print(f"Total image files found: {total_image_count}")
            print(f"Total video files found: {total_video_count}")




async def main():
    checkpoint = load_checkpoint()
    assets_folder_ids = await get_folder_ids_by_name("3954670807", "assets")

    if assets_folder_ids:
        await process_assets_folders(assets_folder_ids[0], resume_from=checkpoint["last_folder"])
        print("Final count:")
        print(f"Total image files found: {total_image_count}")
        print(f"Total video files found: {total_video_count}")
        # os.remove(CHECKPOINT_FILE)  # Remove checkpoint after successful completion
    else:
        print("Assets folder not found")


# Run the async script
asyncio.run(main())


os.remove(CHECKPOINT_FILE)
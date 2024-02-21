import glob
import shutil
import os


total_deleted_folders = 0
all_deleted_contents = []
all_mp3_files = []

MUSIC_PATH = f"/Volumes/NetBackup/Media/"

def clean_files(src_path="", glob_pattern="*/", dry_run=True, first_run=True):
   global all_deleted_contents
   global all_mp3_files
   found_folders = glob.glob(f"{src_path.rstrip('/')}/{glob_pattern}", recursive=True)
   folder_count = len(found_folders)
   if folder_count:
      print(f"Found {folder_count} folder{'s' if folder_count != 1 else ''} in {src_path}")
   if first_run:
      input("Press Enter to start...")
   for index, foldername in enumerate(found_folders, start=1):
      print(f"{index}/{folder_count}: Starting {os.path.dirname(foldername)}")
      if clean_files(foldername, glob_pattern, dry_run, first_run=False):
         if not dry_run:
            try:
               shutil.rmtree(foldername)
               print(f"{foldername} and its contents have been deleted successfully.")
            except OSError as error:
               print(f"Error: {error}. Failed to delete directory.")
         else:
            print(f"{foldername} and its contents would have been deleted.")
         global total_deleted_folders
         total_deleted_folders += 1
      print(f"{index}/{folder_count}: Finished")
      print("---")
   if folder_count == 0:
      children_files = os.listdir(src_path)
      print(children_files)
      if len(children_files) == 1:
         if children_files[0] == '.DS_Store':
            return True
         file_ext = children_files[0].rsplit('.')[-1]
         if file_ext == 'jpg' or file_ext == 'png':
            all_deleted_contents.extend(children_files)
            return True
      if len(children_files) == 0:
         print("Empty folder", src_path, children_files)
         all_deleted_contents.append(src_path)
         return True
      if children_files and any([ x.rsplit('.')[-1] == 'mp3' for x in children_files]) and any([ x.rsplit('.')[-1] == 'm4a' for x in children_files]):
         print("has MP3 and m4a Files")
         all_mp3_files.append(src_path)
         return False
      

IS_DRY_RUN = True
# IS_DRY_RUN = False

clean_files(f"{MUSIC_PATH}audio", dry_run=IS_DRY_RUN)
print(f"Would have or did delete {total_deleted_folders} folders")
with open('out.txt', 'w') as f:
   f.write("\n".join(all_deleted_contents))
with open('mp3.txt', 'w') as f:
   f.write("\n".join(all_mp3_files))
import music_tag
import glob
from pathlib import Path
import shutil
import os




MUSIC_PATH = f"/Volumes/NetBackup/Media/"

def migrate_files(src_path="", dest_path="", glob_pattern="**/*.flac", dry_run=True):
   files = glob.glob(f"{src_path.rstrip('/')}/{glob_pattern}", recursive=True)
   file_count = len(files)
   print(f"Found {file_count} file{'s' if file_count != 1 else ''}")
   input("Press Enter to start...")
   for index, filename in enumerate(files, start=1):
      print(f"{index}/{file_count}: Starting")
      
      base_filename = os.path.basename(filename)
      root_dir = src_path
      folders = []
      file_folder = os.path.dirname(filename)
      while file_folder != root_dir:
         folders.insert(0, os.path.basename(file_folder))
         file_folder = os.path.dirname(file_folder)
      destination = os.path.join(dest_path, *folders, base_filename)
      print(f"Src: {filename}\nDest: {destination}")
      if dry_run:
         print("Would move file")
         print(f"Src: {filename}\nDest: {destination}")
      else:
         print(f"{index}/{file_count}: Moving")
         print(f"Src: {filename}\nDest: {destination}")
         os.makedirs(os.path.dirname(destination), exist_ok=True)
         shutil.move(filename, destination)
      print(f"{index}/{file_count}: Finished")
      print("---")
      

IS_DRY_RUN = True
IS_DRY_RUN = False

migrate_files(f"{MUSIC_PATH}audio", f"{MUSIC_PATH}flac", dry_run=IS_DRY_RUN)
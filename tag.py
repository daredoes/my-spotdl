import music_tag
import glob
from pathlib import Path

MUSIC_PATH = f"/Volumes/NetBackup/Media/music"

def set_metadata(path, data: dict = None, dry_run=False):
    clean_data = {}
    if data is not None:
       data.pop('title', None)
       clean_data = data
    filenames = glob.glob(f"{MUSIC_PATH}/{path}", recursive=True)
    total_file_count = len(filenames)
    print(f"Found {total_file_count} files")
    print(f"Will set the following metadata for these files")
    for k in clean_data.keys():
       print(f"Set '{k}' to '{clean_data[k]}'")
    for index, filename in enumerate(filenames, 1):
      print(f"Starting File {index} of {total_file_count}")
      file_with_metadata =  music_tag.load_file(filename)
      print(f"Modifying '{file_with_metadata['title'] or filename}'")
      print(file_with_metadata)
      if not file_with_metadata['title']:
         if dry_run:
            print(f"Would have set 'title' from '{file_with_metadata['title']}' to '{Path(filename).stem}'")
         else:
          file_with_metadata['title'] = Path(filename).stem
      for k in clean_data.keys():
         if dry_run:
            print(f"Would have set '{k}' from '{file_with_metadata[k]}' to '{clean_data[k]}'")
         else:
          file_with_metadata[k] = clean_data[k]
      if not dry_run:
         file_with_metadata.save()
      print(f"Finished File {index} of {total_file_count}")

IS_DRY_RUN = True
# IS_DRY_RUN = False

set_metadata("**/*.m4a", {
   'genre': 'Soundtrack',
   'album': "Album Name",
   'artist': "Artist Name",
   'albumartist': "Album Artist",
   'year': None
}, dry_run=IS_DRY_RUN)
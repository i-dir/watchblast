import os
import time
import subprocess
from collections import defaultdict
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

watch_dir = r'C:\tmp\playblast'
player = r'C:\Program Files\Keyframe MP 2\bin\KeyframeMP.exe'
filetype = ('.mp4','.avi','.mov')

class ChangeHandler(FileSystemEventHandler):

    files = defaultdict(lambda: 0)

    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif (event.event_type == 'modified' and event.src_path.endswith(filetype)):
            filepath = event.src_path
            oldfilesize = -1
            filesize = os.path.getsize(filepath)

            while filesize != oldfilesize:
                oldfilesize = int(filesize)
                time.sleep(1)
                filesize = os.path.getsize(filepath)

            stats = os.stat(filepath).st_mtime

            if stats - self.files[event.src_path] > 1:
                subprocess.Popen(player + ' "%s"' % filepath)
                self.files[event.src_path] = stats

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(ChangeHandler(), watch_dir, recursive=True)
    observer.start()

    while True:
        time.sleep(1)

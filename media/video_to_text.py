import os
import subprocess
import shutil
import uuid
import tempfile
import time

from media.img_to_text import image_to_text
from system.filesystem.data import add_data, get_data
from commands.extra import clear

from system.filesystem.file_control import save_fs, cwd, get_path, dict_info

from system.errorcontrol.error import er

def video_to_text(path, width=80, fps=10):
    temp_dir = tempfile.mkdtemp()

    try:
        # Extract frames using ffmpeg
        command = [
            "ffmpeg",
            "-i", path,
            "-vf", f"fps={fps},scale={width}:-1",
            f"{temp_dir}/frame_%04d.jpg"
        ]

        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if result.returncode != 0:
            er("ffmpeg failed")
            return None, None

        frames = sorted(os.listdir(temp_dir))
        ascii_frames = []

        for frame_file in frames:
            frame_path = os.path.join(temp_dir, frame_file)

            ascii_frame = image_to_text(frame_path)

            if ascii_frame:
                ascii_frames.append(ascii_frame)

        if not ascii_frames:
            return None, None

        video_data = "\n===FRAME===\n".join(ascii_frames)

        return video_data, fps

    finally:
        # Clean up temp folder
        shutil.rmtree(temp_dir, ignore_errors=True)
        
def vid(*args):
    if len(args) != 2:
        print("usage: vid <input_video's actual path in your system> <name>")
        return
    
    input_path, name = args
    
    current = dict_info()
    
    if not current or current["type"] != "dir":
        er("not a directory")
        return
    
    if not name.endswith(".vid"):
        name += ".vid"
    
    if name in current["children"]:
        er("already exists")
        return
    
    print("processing video... (this may take time)")
    
    video_data, fps = video_to_text(input_path)
    
    if video_data is None:
        er("conversion failed")
        return
    
    loc = str(uuid.uuid4())
    
    current["children"][name] = {
        "type": "vid",
        "size": len(video_data),
        "fps": fps,
        "location": loc
    }
    
    add_data(loc, video_data)
    save_fs()
    
    print(f"video created: {name} at {get_path()}")

def play(name):
    current = dict_info()
    
    if not current or name not in current["children"]:
        er("file not found")
        return
    
    file = current["children"][name]
    
    if file["type"] != "vid":
        er("not a video")
        return
    
    data = get_data(file["location"])
    
    if not data:
        er("empty video")
        return
    
    frames = data.split("\n===FRAME===\n")
    
    fps = file.get("fps", 10)
    delay = 1 / fps if fps > 0 else 0.1
    
    try:
        for frame in frames:
            clear()
            print(frame)
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\nstopped")
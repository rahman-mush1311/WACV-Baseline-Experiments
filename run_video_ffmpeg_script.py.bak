import subprocess
import os
import platform
import shlex

from driver_data_preprocessing import PreProcessingObservations

def get_video_fps(video_path):
    """
    runs the command and captures its output,splits the FPS string like "30000/1001" into numerator and denominator,divides them: 30000 / 1001 ≈ 29.97
    Parameters:
    video_path:  filename along with the file location
    Returns: 
    num / denom: the FPS as a float.
    """
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=r_frame_rate",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    try:
        output = subprocess.check_output(cmd).decode().strip()
        num, denom = map(int, output.split('/'))
        return num / denom
    except Exception as e:
        print(f"Error extracting FPS: {e}")
        return None
        
def run_ffplay_duration(video_path, width, height,start_frame, end_frame, fps, slow_factor):
    """
    runs a video from a specific duration. it is written to see the exact object's movement in the tracked video.
    validates if the video file exsists or not, then calculates time from frames (start_sec, duration), 
    builds a command to run ffplay with the parameters
    [ffplay -ss 5 -autoexit my_video.mp4 -t 10 -vf setpts=2.0*PTS -x 800 -y 600]
    runs that custom command using subprocess.run() where an external program (in this case, ffplay)
    
    Parameters:
    -video_path: filename along with the file location
    -width: 1920
    -height: 1080
    -start_frame: the starting frame number when the object's tracking starts, it is taken from the .txt file (parsed from the .txt file saved in the dictionary)
    -end_frame: the ending frame number when the object's tracking ends, it is taken from the .txt file (parsed from the .txt file saved in the dictionary) 
    -fps: how many indiviual frames are displayed in one second of video (calculated from the get_video_fps function)
    -slow_factor: slow it down by 2X(in our case)
    Returns:
    N/A
    """
    if not os.path.exists(video_path):
        print(f"File not found: {video_path}")
        return
    
    start_sec = start_frame / fps if start_frame is not None else None
    duration = ((end_frame - start_frame) / fps) if start_frame is not None and end_frame is not None else None
    #print(f"{start_sec},{duration}")
    # Build ffplay command
    cmd = ['ffplay']

    # Seek BEFORE input file (faster & more accurate with filters)
    if start_sec is not None:
        cmd += ['-ss', str(start_sec)]

    cmd += ['-autoexit']  # auto-close and quiet output

    # Input video
    cmd += [video_path]

    # Duration (AFTER input)
    if duration is not None:
        cmd += ['-t', str(duration)]

    # Slow motion
    if slow_factor > 1.0:
        cmd += ['-vf', f'setpts={slow_factor}*PTS']

    # Optional window size
    if width and height:
        cmd += ['-x', str(width), '-y', str(height)]

    # Run
    try:
        subprocess.run(cmd)
    except FileNotFoundError:
        print("❌ ffplay not found. Make sure FFmpeg is installed and in your system PATH.")
    except Exception as e:
        print(f"❌ Error running ffplay: {e}")   

def run_ffplay(video_path,width,height):
    """
    run the video from command line taking the video path and adjusts it to the aspect ration in this case 1920 (width), 1080 (height)
    Parameters:
    -video_path: filename along with the file location
    -width: 1920
    -height: 1080
    Returns:
    N/A
    """
    if width and height:
        command = ['ffplay', '-autoexit', video_path, '-x', str(width), '-y', str(height)]
    else:
        command = ['ffplay', '-autoexit', video_path]    
    try:
        subprocess.run(command)
    except FileNotFoundError:
        print(" ffplay not found. Make sure FFmpeg is installed.")


if __name__ == "__main__":
    """
    inputs: 
        trajectory_video_file_name: string of folder path along with filename and extenstion in our case .mp4
        trajectory_txt_filename: string of folder path along with filename and extenstion in our case .txt
        trajectory_object_id: int object id
    output:
        play the video from the location from command line script
    process:
        if the object id is found in the .txt it will extract the start frame and end frame, it will get it's fps then run the video from that time till the end of duration, additionally it will slow down the video and fit into the aspect ratio
        otherwise it will just play the video from the begining to end
    """
    trajectory_video_file_name = input("Enter the video filename with the entire folder path (e.g., C:/data/tracks.mp4):  ").strip()
    trajectory_txt_filename = input("Enter the .txt file name with the entire folder path (e.g., C:/data/tracks.txt): ").strip()
    trajectory_object_id = int(input("Enter the id of the desired object: ").strip())
    
    try:
        with open(trajectory_txt_filename, 'r') as f:
            contents = f.readlines()
        print(f"File loaded: {trajectory_txt_filename} ({len(contents)} lines)")
        file_pre_processor_for_visualization = PreProcessingObservations()
        observations,obs_type=file_pre_processor_for_visualization.load_observations(trajectory_txt_filename)
        if trajectory_object_id in observations:
            print("=== FFplay Video Player ===")
            start_frame_number=observations[trajectory_object_id][0][0]
            end_frame_number=observations[trajectory_object_id][-1][0]
            
            fps=get_video_fps(trajectory_video_file_name)
            print(f"{trajectory_object_id}: {start_frame}-->{end_frame} {fps}")
            run_ffplay_duration(trajectory_video_file_name, 1920, 1080,start_frame_number,end_frame_number,fps,2.0)
        else:
            print(f"the {trajectory_object_id} doesn't exsist")
            run_ffplay(trajectory_video_file_name,1920,1080)
    except FileNotFoundError:
        print(f"File not found: {trajectory_txt_filename}")
    except Exception as e:
        print(f"Error opening file: {e}")
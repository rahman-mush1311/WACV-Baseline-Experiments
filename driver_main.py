from driver_data_preprocessing import PreProcessingObservations

import matplotlib.pyplot as plt
import numpy
import os

def plot_object_trajectories(curr_obs,extracted_ids,filepath,track_type):

    """
    Plots interested objects' trajectory only x and y coordinates.It generates plots one by one
    
    Params:
        - curr_obs: dict of {object_id:[(frame, x, y), ...]}
        - extracted_ids: list of all interested object IDs (subset of keys in observations)
        - filepath: filename with folder locations
        - track_type: 0/1 indicating good/bad track
    Returns:
        N/A
    """
    
    for obj_id in extracted_ids:        
        if obj_id in curr_obs:
            points = curr_obs[obj_id]
            
            x = [p[1] for p in points]  # Extract x-coordinates
            y = [p[2] for p in points]  # Extract y-coordinates
            color = "green" if track_type==1 else "brown"
            plt.plot(x, y, marker="o", linestyle="-", color=color,label=obj_id)  # Plot trajectory

            # Labels & Formatting
            plt.xlabel("X Coordinate")
            plt.ylabel("Y Coordinate")
            plt.title(f"{'GOOD TRACKS' if track_type == 1 else 'BAD TRACKS' }")
            plt.legend()
            plt.grid(True, linestyle="--", alpha=0.6)  
            plt.show()
def open_file_from_user_input():
    
    """
    takes folder location and filename as user input returns the full path to do the parsing
    Params:
    -N/A
    Returns:
    folder_path or None
    """

    folder = input("Enter folder path (e.g., C:/data/tracks): ").strip()
    filename = input("Enter file name (e.g., obj_track_01.txt): ").strip()

    full_path = os.path.join(folder, filename)

    try:
        with open(full_path, 'r') as f:
            contents = f.readlines()
        print(f"File loaded: {filename} ({len(contents)} lines)")
        return full_path
    except FileNotFoundError:
        print(f"File not found: {full_path}")
        return None
    except Exception as e:
        print(f"Error opening file: {e}")
        return None

if __name__ == "__main__":

    file_full_path=open_file_from_user_input()
    observation_processor=PreProcessingObservations()
    
    if file_full_path!=None:
        observations=observation_processor.load_observations(file_full_path)
        print(f"{len(observations)}")
        bad_track_ids,good_track_ids=observation_processor.detect_bad_tracks(observations,90,4096,2160,0.25)
        print(f"{len(bad_track_ids)}")

        plot_object_trajectories(observations,bad_track_ids,file_full_path,0)
        plot_object_trajectories(observations,good_track_ids,file_full_path,1)
    else:
        print(f"!!!Invalid File!!!")


    
        
    
    
    
    
    
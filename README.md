# Static Keyframe Extractor

A Python tool designed to extract unique static keyframes from videos, focusing on stable scenes rather than transitions. This is particularly useful for analyzing screen recordings, such as iOS app demonstrations, by capturing representative frames of distinct application states. Built with OpenCV and NumPy.

## Features
- Detects periods of frame stability to identify key static scenes.
- Configurable parameters:
  - `diff_threshold`: Sensitivity to frame differences.
  - `stability_frames`: Minimum number of consecutive stable frames required.
- Saves keyframes as JPG images in a specified output folder.

## Use Case
Perfect for extracting meaningful screenshots from silent video demos, tutorials, or UI walkthroughs, while ignoring rapid transitions.

## Requirements
- Python 3.x
- OpenCV (`opencv-python`)
- NumPy

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/TMMSantos/static-keyframe-extractor.git
   cd static-keyframe-extractor
   python -m venv keyframes_env
   ```

# Windows
keyframes_env\Scripts\activate
# Linux/Mac
source keyframes_env/bin/activate

2.  Install dependencies:
    
    bash
    
    CollapseWrapCopy
    
    `pip install opencv-python numpy`
    

## Usage

1.  Update the video\_path and output\_folder variables in extract\_static\_keyframes.py with your video file path and desired output directory.
2.  Run the script:
    
    bash
    
    CollapseWrapCopy
    
    `python extract_static_keyframes.py`
    
3.  Check the output folder for extracted keyframes.

## Customization

*   **diff\_threshold**: Lower values (e.g., 5) increase sensitivity to small changes; higher values (e.g., 15) reduce it.
*   **stability\_frames**: Increase (e.g., 30) for longer stable periods; decrease (e.g., 10) for shorter ones.

## Example

For a 30 FPS video, setting stability\_frames=15 requires half a second of stability to save a keyframe. Adjust based on your video's frame rate and content.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements!

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

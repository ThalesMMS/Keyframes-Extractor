# Static Keyframe Extractor

A Python tool that extracts representative keyframes from stable scenes in a video. It is especially useful for screen recordings or UI walkthroughs where each stable view should be captured only once. The project is built with OpenCV and NumPy and can be used as a command-line utility or as a library.

## Features
- Detects periods of frame stability to identify unique scenes.
- Configurable detection parameters (`diff_threshold`, `stability_frames`, `start_index`).
- Saves keyframes as JPG files and reports frame index and timestamp metadata.
- Packaged structure with reusable Python API and CLI entry point.

## Requirements
- Python 3.9 or newer.
- OpenCV (`opencv-python`) and NumPy (installed automatically through the package metadata).

## Installation
```bash
git clone https://github.com/ThalesMMS/Keyframes-Extractor.git
cd Keyframes-Extractor
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -e .
```

That install path enables both the `extract-static-keyframes` command and `python -m static_keyframe_extractor.cli`.

If you only want to run from a source checkout without installing the package, install the runtime dependencies and use `PYTHONPATH=src` when calling the wrapper script:

```bash
pip install -r requirements.txt
PYTHONPATH=src python extract_static_keyframes.py input.mp4 keyframes_out
```

## Usage

### Command line
After `pip install -e .`, run the extractor with the `extract-static-keyframes` command or with `python -m static_keyframe_extractor.cli`:

```bash
extract-static-keyframes input.mp4 keyframes_out \
  --diff-threshold 10 \
  --stability-frames 20 \
  --start-index 100
```

Parameters:
- `video_path`: path to the video you want to analyse.
- `output_folder`: folder where keyframes will be written (created automatically if missing).
- `--diff-threshold`: lower values make the detector more sensitive to small changes (default `12.0`).
- `--stability-frames`: number of consecutive frames under the threshold before saving a keyframe (default `15`).
- `--start-index`: first index used in the output filenames (default `0`).

The command prints each saved keyframe along with the frame index and an approximate timestamp.

From the repository root, you can also use the compatibility script if you either installed the package first or provide `PYTHONPATH=src`:

```bash
PYTHONPATH=src python extract_static_keyframes.py input.mp4 keyframes_out
```

### Python API

```python
from pathlib import Path
from static_keyframe_extractor import extract_static_keyframes

result = extract_static_keyframes(
    Path("input.mp4"),
    Path("keyframes_out"),
    diff_threshold=10.0,
    stability_frames=20,
)

for keyframe in result.keyframes:
    print(f"{keyframe.path} at frame {keyframe.frame_index} ({keyframe.timestamp:.2f}s)")
```

The returned `ExtractionResult` also reports the total number of processed frames and the video FPS (if available).

## Tips
- For high-motion videos, increase `diff_threshold` or `stability_frames` to avoid noise.
- For very static footage, lower the threshold or the required stable frame count to capture shorter transitions.

## Repository layout
- `src/static_keyframe_extractor/`: package with the extractor implementation and CLI.
- `extract_static_keyframes.py`: convenience wrapper to call the CLI without installation.
- `requirements.txt` & `pyproject.toml`: dependency and packaging metadata.

## Contributing
Feel free to open issues or submit pull requests with improvements or new detection strategies.

## License
This project is licensed under the MIT License. See [LICENSE.txt](LICENSE.txt) for details.

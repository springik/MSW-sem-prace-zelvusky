import os

import cv2


def get_frames(video_path, output_directory, frames=10):
    print(f"Processing video {video_path}")
    os.makedirs(output_directory, exist_ok=True)
    capture = cv2.VideoCapture(video_path)
    if not capture.isOpened():
        raise IOError(f"failed to open video file: {video_path}")

    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"\ttotal frames: {total_frames}")

    step = total_frames // frames

    if step == 0:
        step = 1

    for i in range(frames):
        frame_idx = min(i * step, total_frames - 1)
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = capture.read()

        if ret:
            split_path = os.path.basename(video_path).split(".")
            video_name = (
                split_path[0] if len(split_path) == 2
                else split_path[0] + "." + split_path[1]
            )
            output_path = os.path.join(
                output_directory,
                f"{video_name}_frame_{i + 1:02d}.jpg"
            )
            cv2.imwrite(output_path, frame)
            print(f"\tsaving frame {i + 1:02d} to {output_path}")
        else:
            raise IOError(f"failed to read frame {i + 1:02d}; idx:{frame_idx}")

    capture.release()

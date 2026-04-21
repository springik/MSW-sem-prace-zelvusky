import os

import cv2

from lib.frame_acquisition.get_frames import get_frames
from lib.frame_processing.segment import segment

RESOURCES_DIR = './resources'
OUTPUT_DIR = './output'


def main():
    get_frames(f"{RESOURCES_DIR}/videos/C10.24Reh.mkv", f"{RESOURCES_DIR}/frames")
    show_segmented_frames()


def show_segmented_frames():
    for file_path in os.listdir(f"{RESOURCES_DIR}/frames"):
        result, mask = segment(f"{RESOURCES_DIR}/frames/{file_path}")
        #cv2.imshow("Maska", mask)
        cv2.imshow(f"Frame {file_path}", result)
        #cv2.imwrite(f"./docs/postupne_snimky/prvni_snaha/{file_path}", result)
        cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

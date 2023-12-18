import argparse
import os
import shutil
from datetime import datetime
from pathlib import Path

from PIL import Image
from PIL.ExifTags import TAGS
from tqdm.auto import tqdm


class CameraNotConnectedException(Exception):
    pass


def main(args):
    if os.name == "posix":
        input_dir = "/Volumes/Untitled/DCIM/101_PANA/"
    else:
        input_dir = "E:\\DCIM\\101_PANA\\"

    if not check_if_camera_is_connected(input_dir):
        raise CameraNotConnectedException(
            "Camera not found! Check the path or if the camera is connected to the PC!"
        )

    Path(args.output).mkdir(parents=True, exist_ok=True)
    output_dir = args.output
    raw_dir = os.path.join(output_dir, "RAW")
    jpg_dir = os.path.join(output_dir, "JPG")
    all_metadatas = []
    pic_date = ""

    for file_ in Path(input_dir).iterdir():
        if file_.suffix != ".JPG":
            all_metadatas.append((file_.name, pic_date, raw_dir))
        else:
            pic_date = extractMetadata(file_)
            all_metadatas.append((file_.name, pic_date, jpg_dir))

    all_dates = list(set(all_metadatas))

    for _, date, ref_dir in all_dates:
        Path(os.path.join(ref_dir, date)).mkdir(parents=True, exist_ok=True)

    for fname, date, dest_dir in tqdm(all_metadatas):
        input_file = os.path.join(input_dir, fname)
        shutil.copy(input_file, os.path.join(dest_dir, date))


def extractMetadata(file_: Path):
    img = Image.open(file_)
    exif_data = img._getexif()
    exif = {
        TAGS.get(tag): value
        for tag, value in exif_data.items()
        if tag in TAGS and isinstance(TAGS.get(tag), str)
    }
    exif = datetime.strptime(exif["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S")
    exif = exif.strftime("%Y_%m_%d")
    return exif


def check_if_camera_is_connected(input_path):
    return Path(input_path).is_dir()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--output",
        help="output directory",
        default="F:\PC\Foto\Panasonic G9",
        type=str,
    )
    args = parser.parse_args()
    main(args)

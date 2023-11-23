from pathlib import Path
import shutil
import argparse
import os
from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import TAGS
from datetime import datetime

def main(args):
    if os.name == "posix":
        input_dir = "/Volumes/Untitled/DCIM/101_PANA/"
    else:
        input_dir = "E:\\DCIM\\101_PANA\\"
    
    Path(args.output).mkdir(parents=True, exist_ok=True)
    output_dir = args.output
    all_metadatas = []
    pic_date = ""
    last_date = ""

    for file_ in Path(input_dir).iterdir():
        if last_date != pic_date:
            Path(os.path.join(output_dir, last_date)).mkdir(parents=True, exist_ok=True)
            last_date = pic_date
        if file_.suffix != ".JPG":
            all_metadatas.append((file_.name , pic_date))
        pic_date = extractMetadata(file_)
        all_metadatas.append((file_.name , pic_date))

        
    all_dates = list(set(all_metadatas))

    for date in all_dates:
        Path(os.path.join(output_dir, date)).mkdir(parents=True, exist_ok=True)

    for file_ in Path(input_dir).iterdir():
        if file_.suffix != ".JPG":
            print(file_.name, "RAW")
            continue
        
            #shutil.copy(file_, os.path.join(output_dir, date))
        print(file_.name, extractMetadata(file_))


def extractMetadata(file_: Path):
    img = Image.open(file_)
    exif_data = img._getexif()
    exif = {TAGS.get(tag): value for tag, value in exif_data.items()
    if tag in TAGS and isinstance(TAGS.get(tag), str)}
    exif = datetime.strptime(exif["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S")
    exif = exif.strftime("%d%m%Y")
    return exif

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="output directory", default="", type=str, required=True)
    args = parser.parse_args()
    main(args)
import os
import pickle
import cv2
import json
from magic_card_detector import ReferenceImage
import magic_card_detector as mcg
from img_mapping import get_image_filename


input_dir = os.path.join("data", "images")
input_json_path = os.path.join("data", "output.json")
output_hash_path = os.path.join("data", "all_images.dat")
results = []
errors = []
loaded = set()

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))


def process_img(card, filename):
    img = cv2.imread(filename)
    if img is None:
        raise Exception("Could not load {}".format(filename))
    ref = ReferenceImage(filename, img, clahe, meta=card)
    ref.original = None
    ref.clahe = None
    ref.adjusted = None
    return ref


print("Loading previous hash...")
with open(output_hash_path, "rb") as filename:
    hashed_list = pickle.load(filename)
    for ref_im in hashed_list:
        loaded.add(ref_im.name)
        results.append(
            ReferenceImage(ref_im.name, None, clahe, ref_im.phash, meta=ref_im.meta)
        )
print("Loaded {} images".format(len(results)))


def success(processed):
    results.append(processed)
    result_len = len(results)
    if result_len % 1000 == 0:
        print("Processed: {}".format(result_len))


def error(attempt):
    errors.append(attempt)


with open(input_json_path) as input_json:
    to_fetch = json.load(input_json)
    for card in to_fetch:
        for (idx, image) in enumerate(card["images"]):
            filename = os.path.join(input_dir, get_image_filename(card, idx))
            if not os.path.exists(filename):
                error(filename)
                continue

            if filename in loaded:
                continue

            try:
                res = process_img(card, filename)
                success(res)
            except Exception as e:
                print(e)
                error(filename)

with open(output_hash_path, "wb") as f:
    pickle.dump(results, f)

print("Wrote {} results".format(len(results)))
print("Errors: {}".format(errors))

import re
import pathlib
import datetime
import os
import json
import requests
from multiprocessing.pool import ThreadPool
from img_mapping import get_image_filename

input_json = "./data/output.json"
output_dir = "./data"

results = {"success": 0, "failed": []}


def inc_success(_):
    results["success"] += 1


def fail(card, idx, image):
    results["failed"].append(
        {
            "id": card["id"],
            "name": card["name"],
            "image_idx": idx,
            "image": image,
        }
    )


# Ensure images dir
pathlib.Path(os.path.join(output_dir, "images")).mkdir(parents=True, exist_ok=True)


def download_url(url, filename):
    out_name = os.path.join(output_dir, "images", filename)
    if os.path.exists(out_name):
        return

    r = requests.get(url, stream=True)
    if r.status_code == requests.codes.ok:
        with open(out_name, "wb") as out:
            for data in r:
                out.write(data)


pool = ThreadPool(15)

with open("./data/output.json") as input_json:
    to_fetch = json.load(input_json)
    for idx, card in enumerate(to_fetch):
        if idx % 1000:
            print("Fetching {}...".format(idx))
        for (idx, image) in enumerate(card["images"]):
            filename = get_image_filename(card["set"], idx)
            pool.apply_async(
                download_url,
                args=[image, filename],
                callback=inc_success,
                error_callback=lambda x: fail(card, idx, image),
            )


# Wait for tasks to finish
pool.close()
pool.join()

print(results)

results_name = os.path.join(
    output_dir, "get_images_results_{}.json".format(datetime.datetime.now().isoformat())
)
with open(results_name, "w") as output_json:
    json.dump(results, output_json)

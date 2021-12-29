import glob
import os
import pathlib
from PIL import Image
from multiprocessing.pool import ThreadPool

input_glob = os.path.join("data", "binder-2021-12-28", "*.jpg")
output_dir = os.path.join("data", "binder-2021-12-28-rotated")

# Ensure images dir
pathlib.Path(os.path.join(output_dir)).mkdir(parents=True, exist_ok=True)

cw_list = {
    "PXL_20211228_180807982.MP.jpg",
    "PXL_20211228_180920126.MP.jpg",
    "PXL_20211228_180925942.jpg",
    "PXL_20211228_180929103.jpg",
    "PXL_20211228_180934869.MP.jpg",
    "PXL_20211228_180941006.jpg",
    "PXL_20211228_180945121.jpg",
    "PXL_20211228_180952167.MP.jpg",
    "PXL_20211228_181002300.jpg",
    "PXL_20211228_181007716.MP.jpg",
    "PXL_20211228_181011345.jpg",
    "PXL_20211228_181017553.MP.jpg",
    "PXL_20211228_181024966.MP.jpg",
}

pool = ThreadPool(8)

results = {"success": 0, "errors": []}


def process_image(file):
    base = os.path.basename(file)
    im = Image.open(file)
    if os.path.basename(file) in cw_list:
        im.rotate(-90, expand=True).save(os.path.join(output_dir, base))
    else:
        im.rotate(90, expand=True).save(os.path.join(output_dir, base))

    print("Processed: {}".format(file))
    results["success"] += 1


for file in glob.glob(input_glob):
    pool.apply_async(
        process_image, args=[file], error_callback=lambda e: results["errors"].append(e)
    )

pool.close()
pool.join()
print(results)

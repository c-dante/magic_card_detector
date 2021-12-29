import re


def get_image_filename(card, img_idx):
    return "{}_{}_{}_{}.jpg".format(
        card["set"], re.sub("[\W]+", "_", card["name"]), card["id"], img_idx
    )

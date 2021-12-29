import json
import json_stream

output = []


def get_image(item):
    layout = item["layout"]
    if layout in ["transform", "modal_dfc", "double_faced_token"]:
        return [x["image_uris"]["normal"] for x in item["card_faces"]]

    try:
        return [item["image_uris"]["normal"]]
    except KeyError:
        print(item["layout"])
        print(item["name"])
        print(item["card_faces"])
        print(item["scryfall_uri"])
        raise Exception("oops")


with open("./data/unique-artwork-20211228101258.json") as input_json:
    data = json_stream.load(input_json)
    for item in data.persistent():
        if item["lang"] != "en":
            continue

        if item["layout"] in [
            "planar",
            "scheme",
            "vanguard",
            "art_series",
            "reversible_card",
        ]:
            continue

        output.append(
            {
                "name": item["name"],
                "id": item["id"],
                "set": item["set"],
                "images": get_image(item),
            }
        )

with open("./data/output.json", "w") as output_json:
    json.dump(output, output_json)

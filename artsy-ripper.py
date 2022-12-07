# This is a script that rips high res pictures from Artsy

import math
import argparse
import requests
from PIL import Image

def rip(in_url):
    # Find the tile directory
    r = requests.get(in_url)
    end_i = r.text.find("large.jpg")
    start_i = r.text.find("https", end_i - 100, end_i)
    tile_url = r.text[start_i:end_i].replace("%3A", ":").replace("%2F", "/") + "dztiles/"
    print("Tile URL: {}".format(tile_url))

    # Find the highest resolution tile subdirectory
    target_level = None
    for level in range(20, 0, -1):
        r = requests.get(tile_url + str(level) + "/0_0.jpg", stream=True)
        if r.ok:
            target_level = level
            break
    
    print("Highest resolution level found: {}".format(target_level))

    # Rip tiles
    target_url = tile_url + str(target_level) + "/"
    u, v, max_u, max_v = 0, 0, 0, 0
    finished = False
    images = list()
    while True:
        while True:
            response = requests.get(target_url + str(u) + "_" + str(v) + ".jpg", stream=True)
            if not response.ok:
                print(response)
                if v == 0: finished = True
                break
            
            with open("pic" + str(u) + "_" + str(v) + ".jpg", "wb") as handle:
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
            
            images.append(Image.open("pic" + str(u) + "_" + str(v) + ".jpg"))

            max_u = u
            max_v = v
            v += 1
        
        if finished: break
        u += 1
        v = 0

    print("Downloaded {} ({} x {}) tiles".format((max_u + 1) * (max_v + 1), max_u + 1, max_v + 1))

    # Stitch tiles
    out_height = images[0].size[1] * max_v + images[len(images) - 1].size[1]
    out_width = images[0].size[0] * max_u + images[len(images) - 1].size[0]
    im_out = Image.new("RGB", (out_width, out_height))
    for i, im in enumerate(images):
        u = math.floor(i / (max_v + 1))
        v = i % (max_v + 1)
        im_out.paste(im, (u * images[0].size[0], v * images[0].size[1]))
    
    im_out.save(in_url.replace("https://www.artsy.net/artwork/", "") + "_stitched.jpg")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True)
    args = parser.parse_args()
    rip(args.url)
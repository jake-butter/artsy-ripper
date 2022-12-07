# This is a script that rips high res pictures from Artsy

import requests
from PIL import Image
import math

def main():
    url_root = "https://d32dm0rphc51dk.cloudfront.net/ZbWUyc5zzdkdxKOoJz4bnA/dztiles/12/"
    u,v, max_u, max_v = 0, 0, 0, 0
    finito = False
    immos = list()
    while True:
        while True:
            response = requests.get(url_root + str(u) + "_" + str(v) + ".jpg", stream=True)
            if not response.ok:
                print(response)
                if v == 0: finito = True
                break
            
            bad_count = 0
            with open("pic" + str(u) + "_" + str(v) + ".jpg", "wb") as handle:
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
            immos.append(Image.open("pic" + str(u) + "_" + str(v) + ".jpg"))
            max_u = u
            max_v = v
            v += 1
        if finito: break
        u += 1
        v = 0

    print("Download complete \n")
    print("Dimensions are {} by {}\n".format(max_u + 1, max_v + 1))

    out_height = immos[0].size[1] * max_v + immos[len(immos) - 1].size[1]
    out_width = immos[0].size[0] * max_u + immos[len(immos) - 1].size[0]
    im_out = Image.new("RGB", (out_width, out_height))
    for i, im in enumerate(immos):
        u = math.floor(i / (max_v + 1))
        v = i % (max_v + 1)
        im_out.paste(im, (u * immos[0].size[0], v * immos[0].size[1]))
    im_out.save("output.jpg")

if __name__ == "__main__":
    main()
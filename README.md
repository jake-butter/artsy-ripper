# Artsy Ripper
Ripper for high-resolution images found on artsy.net.

Artsy displays high-resolution images as a series of tiles, so if you try to save these images in a browser you only get a section of the whole image. This script automatically finds the highest resolution tiles, downloads them, and combines them into a single image for your convenience.

## Usage Instructions
1. Install dependencies: Requests, Pillow
2. Run script, providing artwork URL:  
```
python .\artsy-ripper.py --url https://www.artsy.net/artwork/christina-tsaou-playful-peaceful
```

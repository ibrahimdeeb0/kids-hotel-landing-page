"""Extract the supplied PDF artwork and produce web-sized copies without redrawing it.

Usage: python3 scripts/extract-logo.py '/path/to/Kids hotel.pdf'
Requires pypdf and Pillow only when re-extracting the source artwork.
"""
from pathlib import Path
import sys
from pypdf import PdfReader
from PIL import Image

root = Path(__file__).resolve().parent.parent
images = list(PdfReader(sys.argv[1]).pages[0].images)
if len(images) != 1:
    raise ValueError('Expected one embedded logo image; review the PDF before extraction.')
logo = images[0].image.convert('RGB')
for size in (480, 960):
    logo.resize((size, size), Image.Resampling.LANCZOS).save(
        root / f'assets/kids-hotel-logo-{size}.webp', 'WEBP', quality=92, method=6,
    )
logo.resize((64, 64), Image.Resampling.LANCZOS).save(root / 'assets/favicon.png')
print('Extracted original artwork; generated 480px, 960px and favicon assets.')

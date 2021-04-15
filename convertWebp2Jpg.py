import argparse
from PIL import Image

parser = argparse.ArgumentParser(description='Covert WEBP to jpg.')
parser.add_argument('-i', '--inputfile', required=True, nargs=1, help=("Input Filename"))

args = parser.parse_args()

fileName = args.inputfile[0]

im = Image.open(fileName)
if im.format == "WEBP":
    im.convert('RGB')
    im.save(fileName,'jpeg')

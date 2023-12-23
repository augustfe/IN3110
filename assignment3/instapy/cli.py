"""Command-line (script) interface to instapy"""

import argparse
import sys

import numpy as np
from PIL import Image

import instapy
from . import io, timing


def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python",
    filter: str = "color2gray",
    scale: int = 1,
    runtime: bool = False,
) -> None:
    """Run the selected filter"""
    # load the image from a file
    image = io.read_image(file)
    if scale != 1:
        # Resize image, if needed
        im = Image.open(file)
        resized = im.resize((im.width // scale, im.height // scale))
        image = np.asarray(resized)

    # Apply the filter
    filter_func = instapy.get_filter(filter, implementation)
    if runtime:
        time = timing.time_one(filter_func, image)
        print(f"Average time over 3 runs: {time}s")
    filtered = filter_func(image)
    if out_file:
        # save the file
        io.write_image(filtered, out_file)
    else:
        # not asked to save, display it instead
        io.display(filtered)


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Apply a filter to an image")

    # filename is positional and required
    parser.add_argument("file", help="The filename to apply filter to")
    parser.add_argument("-o", "--out", metavar="OUT", help="The output filename")

    # Add required arguments
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", "--gray", action="store_true", help="Select gray filter")
    group.add_argument(
        "-se", "--sepia", action="store_true", help="Select sepia filter"
    )
    parser.add_argument(
        "-sc",
        "--scale",
        metavar="SCALE",
        default=1,
        type=int,
        help="Factor to scale image by",
    )
    parser.add_argument(
        "-i",
        "--implementation",
        choices=["python", "numpy", "numba"],
        default="numpy",
        help="The implementation",
    )
    parser.add_argument(
        "-r",
        "--runtime",
        action="store_true",
        help="Average runtime of chosen implementation",
    )

    # parse arguments and call run_filter
    args = parser.parse_args()

    filter = "color2sepia" if args.sepia else "color2gray"
    run_filter(
        args.file,
        out_file=args.out,
        implementation=args.implementation,
        filter=filter,
        scale=args.scale,
        runtime=args.runtime,
    )

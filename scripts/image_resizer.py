#!/usr/bin/env python3

import os
import argparse
from PIL import Image

def resize_image(input_path, output_path, max_dimension):
    """
    Resizes an image to a maximum width or height while maintaining aspect ratio.
    """
    try:
        with Image.open(input_path) as img:
            # Get original dimensions
            width, height = img.size

            # If the image is already smaller than the max dimension, do nothing
            if width <= max_dimension and height <= max_dimension:
                print(f"Skipping {os.path.basename(input_path)} (already small enough).")
                # If the output path is different, we still save a copy
                if input_path != output_path:
                    img.save(output_path, optimize=True)
                return

            # Determine which dimension is larger and calculate the new size
            if width > height:
                new_width = max_dimension
                new_height = int(max_dimension * height / width)
            else:
                new_height = max_dimension
                new_width = int(max_dimension * width / height)

            # Resize the image
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save the resized image with optimization
            # For JPEGs, 'quality' can be adjusted (1-95).
            if output_path.lower().endswith(('.jpg', '.jpeg')):
                resized_img.save(output_path, quality=85, optimize=True)
            else:
                resized_img.save(output_path, optimize=True)
                
            print(f"Resized {os.path.basename(input_path)} -> {new_width}x{new_height}px")

    except IOError:
        print(f"Error: Cannot open or process file {input_path}")

def main():
    """
    Main function to parse arguments and process images.
    """
    parser = argparse.ArgumentParser(description="Resize images for websites automatically.")
    parser.add_argument("input", help="Input image file or directory of images.")
    parser.add_argument("output", help="Output directory for resized images.")
    parser.add_argument("--max_dim", type=int, default=1200, help="Maximum width or height in pixels (default: 1200).")

    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)
        print(f"Created output directory: {args.output}")

    # Check if input is a directory or a single file
    if os.path.isdir(args.input):
        print(f"Processing all images in directory: {args.input}")
        for filename in os.listdir(args.input):
            input_path = os.path.join(args.input, filename)
            # Make sure it's a file and a supported image type
            if os.path.isfile(input_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                output_path = os.path.join(args.output, filename)
                resize_image(input_path, output_path, args.max_dim)
    elif os.path.isfile(args.input):
        print(f"Processing a single file: {args.input}")
        filename = os.path.basename(args.input)
        output_path = os.path.join(args.output, filename)
        resize_image(args.input, output_path, args.max_dim)
    else:
        print(f"Error: Input path '{args.input}' is not a valid file or directory.")

if __name__ == "__main__":
    main()
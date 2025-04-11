# Import necessary libraries
import os
from PIL import Image
import argparse

# Define standard folder names relative to the script location
INPUT_FOLDER = "inputs"
OUTPUT_FOLDER = "outputs"

def convert_webp_to_png_and_jpeg(base_filename, quality=85):
    """
    Looks for base_filename.webp in the INPUT_FOLDER, converts it to both PNG
    and JPEG formats, and saves them into the OUTPUT_FOLDER.

    Args:
        base_filename (str): The base name of the input file (without extension).
                                Example: 'my_image' for 'inputs/my_image.webp'.
        quality (int): The quality setting for JPEG conversion (1-100). Default 85.

    Returns:
        bool: True if the process runs to completion (both conversions attempted),
              False if the input file is not found or a critical error occurs early.
              Note: Individual PNG/JPEG conversion errors are printed but don't stop
              the other conversion attempt.
    """
    input_path = os.path.join(INPUT_FOLDER, base_filename)

    
    # Remove the extension from the base_filename ".webp"
    if base_filename.endswith(".webp"):
        str_core_filename = base_filename[:-5]
    else:
        str_core_filename = base_filename
    
    output_png_path = os.path.join(OUTPUT_FOLDER, str_core_filename + ".png")
    output_jpg_path = os.path.join(OUTPUT_FOLDER, str_core_filename + ".jpg") # Use .jpg

    try:
        # 1. Validate input path
        if not os.path.isfile(input_path): # More specific check for file
            print(f"Error: Input file not found at '{input_path}'")
            return False

        print(f"Processing '{input_path}'...")

        # 2. Ensure output directory exists
        os.makedirs(OUTPUT_FOLDER, exist_ok=True) # Creates dir if not exists

        # 3. Open the WebP image
        img = Image.open(input_path)

        # --- PNG Conversion ---
        png_success = False
        try:
            print(f"Converting to PNG -> '{output_png_path}'")
            # Save directly (PNG supports transparency)
            img.save(output_png_path, format='PNG')
            print(" -> PNG conversion successful.")
            png_success = True
        except Exception as e_png:
            print(f" !! Error converting to PNG: {e_png}")

        # --- JPEG Conversion ---
        jpg_success = False
        try:
            print(f"Converting to JPEG -> '{output_jpg_path}' (Quality: {quality})")
            img_for_jpeg = img # Start with the original

            # Handle transparency if needed (JPEG doesn't support it)
            if img_for_jpeg.mode == 'RGBA':
                print("   (Input has transparency, adding white background for JPEG)")
                # Create a white background image
                bg = Image.new("RGB", img_for_jpeg.size, (255, 255, 255))
                # Paste the RGBA image onto the white background using alpha mask
                bg.paste(img_for_jpeg, mask=img_for_jpeg.split()[3])
                img_for_jpeg = bg # Use the merged image
            # Ensure image is in RGB mode if it wasn't RGBA (e.g., P mode)
            elif img_for_jpeg.mode != 'RGB':
                 img_for_jpeg = img_for_jpeg.convert('RGB')

            # Save as JPEG
            img_for_jpeg.save(output_jpg_path, format='JPEG', quality=quality)
            print(" -> JPEG conversion successful.")
            jpg_success = True
        except Exception as e_jpg:
            print(f" !! Error converting to JPEG: {e_jpg}")

        print(f"Finished processing '{base_filename}'. PNG: {'OK' if png_success else 'Failed'}, JPEG: {'OK' if jpg_success else 'Failed'}")
        return True # Function completed its attempts

    except Exception as e:
        # Catch other potential errors (e.g., PIL issues, permissions)
        print(f"An unexpected error occurred processing '{base_filename}': {e}")
        return False

# --- Command-Line Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=f"Convert image_name.webp from './{INPUT_FOLDER}/' folder to both PNG and JPEG formats, saving them into the './{OUTPUT_FOLDER}/' folder."
    )
    parser.add_argument(
        "-f", "--filename",
        required=True,
        help=f"Base filename of the WebP image (e.g., 'my_image' for '{INPUT_FOLDER}/my_image.webp')."
    )
    parser.add_argument(
        "-q", "--quality",
        type=int,
        default=100,
        help="JPEG quality setting (1-100, default: 100)."
    )

    args = parser.parse_args()

    # Validate quality range
    if not (1 <= args.quality <= 100):
        print("Error: Quality must be between 1 and 100.")
    else:
        # Call the conversion function with the base filename
        convert_webp_to_png_and_jpeg(args.filename, args.quality)
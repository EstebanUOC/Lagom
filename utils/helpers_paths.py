#utils/helpers_paths.py
import os
import sys

def resource_path(relative_path, external_override=True):
    """
    Get absolute path to a resource.

    If running from a PyInstaller bundle, it checks first for the file in the current
    working directory (alongside the .exe). If not found and external_override is False,
    falls back to the internal bundled path.

    If running from source (not frozen), loads from the project directory.
    """
    if getattr(sys, 'frozen', False):  # Running as bundled executable
        if external_override:
            external_path = os.path.join(os.getcwd(), relative_path)
            if os.path.exists(external_path):
                return external_path
        # Fallback to the bundled path
        base_path = sys._MEIPASS
    else:
        # Running in development (not bundled)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    return os.path.join(base_path, relative_path)


def get_resource_path(global_path, filename):
    """this function builds a complete file path for an image button, taking two arguments:
        global_path: The base path to the folder where the image button is located.
        filename: The name of the image file (e.g., 'btn_play.png')."""
    return resource_path(os.path.join(global_path, filename))


def read_images(path, indexes=None, not_static_image=0):
    images_list = []
    if indexes is None:
        # Load all images if no specific indexes are provided
        indexes = range(0, count_items(path) + not_static_image)

    for i in indexes:
        image_path = os.path.join(path, f'img ({i}).png')
        images_list.append(image_path)

    return images_list

def count_items(path):
    """Count how many files are in the given folder."""
    try:
        return len([
            f for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f))
        ])
    except FileNotFoundError:
        print(f"[count_items] Path not found: {path}")
        return 0

def load_image_paths(path, image_name):
    new_path = get_resource_path(path, image_name)
    print(f"[load_image_paths] Loading image path: {new_path}")
    return new_path
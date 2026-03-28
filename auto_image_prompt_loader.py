import os
import random
from PIL import Image
import numpy as np

class AutoImageCaptionBatchLoaderNoCache:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {"default": ""}),
                "batch_size": ("INT", {"default": 1, "min": 0, "max": 9999}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("images", "captions")
    FUNCTION = "load_pairs"
    CATEGORY = "utils"

    def load_pairs(self, folder_path, batch_size, seed):
        if not os.path.exists(folder_path):
            return ([], [""])

        # Supported image formats
        image_exts = (".png", ".jpg", ".jpeg", ".webp")

        # Find image files
        image_files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith(image_exts)
        ]

        if not image_files:
            return ([], [""])

        # Pair images with captions
        pairs = []
        for img_file in image_files:
            base = os.path.splitext(img_file)[0]
            txt_path = os.path.join(folder_path, base + ".txt")
            img_path = os.path.join(folder_path, img_file)

            if not os.path.exists(txt_path):
                continue

            pairs.append((img_path, txt_path))

        if not pairs:
            return ([], [""])

        # Shuffle deterministically
        random.seed(seed)
        random.shuffle(pairs)

        # Apply batch size
        if batch_size != 0:
            pairs = pairs[:batch_size]

        images = []
        captions = []

        for img_path, txt_path in pairs:
            try:
                # Load image
                img = Image.open(img_path).convert("RGB")
                img = np.array(img).astype(np.float32) / 255.0
                images.append(img)

                # Load caption
                with open(txt_path, "r", encoding="utf-8") as f:
                    caption = f.read().strip()
                    captions.append(caption)

            except:
                continue

        if not images:
            return ([], [""])

        return (images, captions)


NODE_CLASS_MAPPINGS = {
    "AutoImageCaptionBatchLoaderNoCache": AutoImageCaptionBatchLoaderNoCache
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AutoImageCaptionBatchLoaderNoCache": "Auto Image+Caption Loader (No Cache)"
}
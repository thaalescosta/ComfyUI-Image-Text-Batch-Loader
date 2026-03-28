import os
import random
from PIL import Image
import numpy as np
import torch

class AutoImageTextBatchLoaderNoCache:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {"default": ""}),
                "batch_size": ("INT", {"default": 0, "min": 0, "max": 9999}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("images", "texts")
    OUTPUT_IS_LIST = (True, True)
    FUNCTION = "load_pairs"
    CATEGORY = "utils"

    @classmethod
    def _empty_return(cls):
        blank = torch.zeros(1, 1, 1, 3)
        return ([blank], [""])

    def load_pairs(self, folder_path, batch_size, seed):
        if not os.path.exists(folder_path):
            print(f"[Auto Image+Text Loader] Invalid folder: {folder_path}")
            return self._empty_return()

        # Supported image formats
        image_exts = (".png", ".jpg", ".jpeg", ".webp")

        # Find image files
        image_files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith(image_exts)
        ]

        if not image_files:
            print(f"[Auto Image+Text Loader] No images found in: {folder_path}")
            return self._empty_return()

        # Pair images with texts
        pairs = []
        for img_file in image_files:
            base = os.path.splitext(img_file)[0]
            txt_path = os.path.join(folder_path, base + ".txt")
            img_path = os.path.join(folder_path, img_file)

            if not os.path.exists(txt_path):
                continue

            pairs.append((img_path, txt_path))

        if not pairs:
            print(f"[Auto Image+Text Loader] No image+text pairs found in: {folder_path}")
            return self._empty_return()

        # Shuffle deterministically
        random.seed(seed)
        random.shuffle(pairs)

        # Apply batch size
        if batch_size != 0:
            pairs = pairs[:batch_size]

        images = []
        texts = []

        for img_path, txt_path in pairs:
            try:
                # Load image
                img = Image.open(img_path).convert("RGB")
                img = np.array(img).astype(np.float32) / 255.0
                img = torch.from_numpy(img)[None,]
                images.append(img)

                # Load text
                with open(txt_path, "r", encoding="utf-8") as f:
                    text = f.read().strip()
                    texts.append(text)

            except Exception as e:
                print(f"[Auto Image+Text Loader] Failed to load {img_path}: {e}")
                continue

        if not images:
            print(f"[Auto Image+Text Loader] All pairs failed to load in: {folder_path}")
            return self._empty_return()

        return (images, texts)


NODE_CLASS_MAPPINGS = {
    "AutoImageTextBatchLoaderNoCache": AutoImageTextBatchLoaderNoCache
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AutoImageTextBatchLoaderNoCache": "Auto Image+Text Batch Loader (No Cache)"
}

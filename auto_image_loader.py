import os
import re
from PIL import Image
import numpy as np
import torch

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]

class AutoImageBatchLoader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {"default": ""}),
                "batch_size": ("INT", {"default": 0, "min": 0, "max": 1000}),  # 0 = all
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "load_images"
    CATEGORY = "utils"

    def load_images(self, folder_path, seed, batch_size):
        _ = seed  # trigger recompute

        if not os.path.isdir(folder_path):
            print(f"[Auto Image Loader] Invalid folder: {folder_path}")
            return ([],)

        # Filter only image files
        files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
        ]

        # Natural sort
        files = sorted(files, key=natural_sort_key)

        total_files = len(files)

        # Apply batch logic
        if batch_size > 0:
            files = files[:batch_size]
        # else: batch_size == 0 → keep all files

        image_list = []

        for file in files:
            full_path = os.path.join(folder_path, file)

            try:
                img = Image.open(full_path).convert("RGB")
                img = np.array(img).astype(np.float32) / 255.0
                img = torch.from_numpy(img)[None,]
                image_list.append(img)
            except Exception as e:
                print(f"Failed to load {file}: {e}")

        print(f"[Auto Loader] Loaded {len(image_list)} / {total_files} images")

        return (image_list,)


NODE_CLASS_MAPPINGS = {
    "AutoImageBatchLoader": AutoImageBatchLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AutoImageBatchLoader": "Auto Image Batch Loader (No Cache)"
}
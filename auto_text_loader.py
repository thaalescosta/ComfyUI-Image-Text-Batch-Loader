import os
import re
import random

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]

class AutoTextBatchLoaderNoCache:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {"default": ""}),
                "batch_size": ("INT", {"default": 0, "min": 0, "max": 9999}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "sort_order": (["alphabetical", "reverse alphabetical", "random"],),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("texts",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "load_texts"
    CATEGORY = "utils"

    def load_texts(self, folder_path, batch_size, seed, sort_order):
        _ = seed  # trigger recompute only

        if not os.path.exists(folder_path):
            return ([""],)

        # Always re-read files (NO CACHE)
        files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith(".txt")
        ]

        if not files:
            return ([""],)

        # Sort or shuffle
        if sort_order == "random":
            random.shuffle(files)
        elif sort_order == "reverse alphabetical":
            files = sorted(files, key=natural_sort_key, reverse=True)
        else:
            files = sorted(files, key=natural_sort_key)

        # Load all texts
        texts = []
        for file in files:
            try:
                with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        texts.append(content)
            except Exception as e:
                print(f"[Auto Text Loader] Failed to read {file}: {e}")
                continue

        if not texts:
            return ([""],)

        # Apply batch_size logic
        if batch_size == 0:
            selected = texts
        else:
            selected = texts[:batch_size]

        return (selected,)


NODE_CLASS_MAPPINGS = {
    "AutoTextBatchLoaderNoCache": AutoTextBatchLoaderNoCache
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AutoTextBatchLoaderNoCache": "Auto Text Batch Loader (No Cache)"
}
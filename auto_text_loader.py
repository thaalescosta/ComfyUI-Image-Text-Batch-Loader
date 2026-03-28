import os
import random

class AutoTextBatchLoaderNoCache:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {"default": ""}),
                "batch_size": ("INT", {"default": 0, "min": 0, "max": 9999}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("texts",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "load_texts"
    CATEGORY = "utils"

    def load_texts(self, folder_path, batch_size, seed):
        if not os.path.exists(folder_path):
            return ([""],)

        # Always re-read files (NO CACHE)
        files = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith(".txt")
        ]

        if not files:
            return ([""],)

        # Deterministic shuffle using seed
        random.seed(seed)
        random.shuffle(files)

        # Load all texts
        texts = []
        for file in files:
            try:
                with open(file, "r", encoding="utf-8") as f:
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
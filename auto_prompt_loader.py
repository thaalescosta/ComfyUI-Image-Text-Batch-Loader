import os
import random

class AutoPromptBatchLoaderNoCache:
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
    RETURN_NAMES = ("prompts",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "load_prompts"
    CATEGORY = "utils"

    def load_prompts(self, folder_path, batch_size, seed):
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

        # Load all prompts
        prompts = []
        for file in files:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        prompts.append(content)
            except Exception as e:
                print(f"[Auto Prompt Loader] Failed to read {file}: {e}")
                continue

        if not prompts:
            return ([""],)

        # Apply batch_size logic
        if batch_size == 0:
            selected = prompts
        else:
            selected = prompts[:batch_size]

        return (selected,)


NODE_CLASS_MAPPINGS = {
    "AutoPromptBatchLoaderNoCache": AutoPromptBatchLoaderNoCache
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AutoPromptBatchLoaderNoCache": "Auto Prompt Batch Loader (No Cache)"
}
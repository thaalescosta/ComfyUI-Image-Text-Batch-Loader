# ComfyUI Image Text Batch Loader

A set of custom nodes for ComfyUI that load images and/or text prompts from a folder in batch, without caching — so changes on disk are always picked up on each run.

## Nodes

### Auto Image Batch Loader (No Cache)
Loads images from a folder and returns them as a list.

| Input | Type | Description |
|---|---|---|
| `folder_path` | STRING | Path to the folder containing images |
| `batch_size` | INT | Number of images to load. `0` = load all |
| `seed` | INT | Triggers re-evaluation on change |

- Supports `.png`, `.jpg`, `.jpeg`, `.webp`
- Files are sorted in natural order (e.g. `img2` before `img10`)

---

### Auto Image+Text Batch Loader (No Cache)
Loads image + `.txt` text pairs from a folder. Only pairs where both files exist are loaded.

| Input | Type | Description |
|---|---|---|
| `folder_path` | STRING | Path to the folder containing image/prompt pairs |
| `batch_size` | INT | Number of pairs to load. `0` = load all |
| `seed` | INT | Controls shuffle order deterministically |

- Pairs are shuffled deterministically using the seed
- Supports `.png`, `.jpg`, `.jpeg`, `.webp` images with matching `.txt` files

---

### Auto Text Batch Loader (No Cache)
Loads `.txt` files from a folder and returns their contents as a list of strings.

| Input | Type | Description |
|---|---|---|
| `folder_path` | STRING | Path to the folder containing `.txt` files |
| `batch_size` | INT | Number of texts to load. `0` = load all |
| `seed` | INT | Controls shuffle order deterministically |

- Files are shuffled deterministically using the seed
- Empty files are skipped

## Installation

Clone into your ComfyUI `custom_nodes` folder:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/thaalescosta/ComfyUI-Image-Text-Batch-Loader
```

Then restart ComfyUI.

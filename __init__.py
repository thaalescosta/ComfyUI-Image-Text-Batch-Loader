from .auto_image_loader import NODE_CLASS_MAPPINGS as _img_cls, NODE_DISPLAY_NAME_MAPPINGS as _img_disp
from .auto_prompt_loader import NODE_CLASS_MAPPINGS as _prompt_cls, NODE_DISPLAY_NAME_MAPPINGS as _prompt_disp
from .auto_image_prompt_loader import NODE_CLASS_MAPPINGS as _imgprompt_cls, NODE_DISPLAY_NAME_MAPPINGS as _imgprompt_disp

NODE_CLASS_MAPPINGS = {**_img_cls, **_prompt_cls, **_imgprompt_cls}
NODE_DISPLAY_NAME_MAPPINGS = {**_img_disp, **_prompt_disp, **_imgprompt_disp}
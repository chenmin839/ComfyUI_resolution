from .nodes import AspectRatioLatentImage

NODE_CLASS_MAPPINGS = {
    "AspectRatioLatentImage": AspectRatioLatentImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AspectRatioLatentImage": "Cm Latent Image",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 
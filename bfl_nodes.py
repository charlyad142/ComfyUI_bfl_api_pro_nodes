from .bfl_utils import *
import requests
import torch

class BFL_ImageGenerator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "width": ("INT", {"default": 1024, "min": 512, "max": 2048}),
                "height": ("INT", {"default": 768, "min": 512, "max": 2048}),
                "api_version": (["1.1"], {"default": "1.1"}),
                "safety_tolerance": ("INT", {"default": 2, "min": 0, "max": 6}),
                "output_format": (["jpeg", "png"], {"default": "jpeg"}),
                "x_key": ("STRING", {"default": ""}),
            },
            "optional": {
                "seed": ("INT", {"default": 30}),
                "image_prompt": ("IMAGE",),
                "steps": ("INT", {"default": 40, "min": 15, "max": 50}),
                "guidance": ("FLOAT", {"default": 2.5, "min": 1.0, "max": 100.0}),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING")
    FUNCTION = "generate"
    CATEGORY = "BFL/Generation"

    def generate(self, **kwargs):
        try:
            config = BFLConfigLoader()
            endpoint = "flux-pro-1.1" if kwargs['api_version'] == "1.1" else "flux-pro-1.1"
            
            payload = {
                "prompt": kwargs['prompt'],
                "width": kwargs['width'],
                "height": kwargs['height'],
                "safety_tolerance": kwargs['safety_tolerance'],
                "output_format": kwargs['output_format'],
                "seed": kwargs['seed'] if kwargs['seed'] != -1 else None,
            }
            
            if kwargs['api_version'] == "1.0":
                payload.update({
                    "steps": kwargs.get('steps', 40),
                    "guidance": kwargs.get('guidance', 2.5),
                })
            
            if 'image_prompt' in kwargs and kwargs['image_prompt'] is not None:
                payload['image_prompt'] = image_to_base64(kwargs['image_prompt'])
            
            response = requests.post(
                url=f"https://api.bfl.ai/v1/{endpoint}",
                headers={"x-key": config.get_api_key(kwargs['x_key']), "Content-Type": "application/json"},
                json={k: v for k, v in payload.items() if v is not None},
                timeout=30
            )
            
            return handle_api_response_with_status(response, kwargs['output_format'], kwargs['x_key'])
        
        except Exception as e:
            error_msg = str(e)
            print(f"BFL Generation Error: {error_msg}")
            return (create_error_image(), f"✗ Error: {error_msg}")

class BFL_Inpainting:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
                "prompt": ("STRING", {"multiline": True}),
                "steps": ("INT", {"default": 50, "min": 15, "max": 50}),
                "guidance": ("FLOAT", {"default": 60.0, "min": 1.0, "max": 100.0}),
                "output_format": (["jpeg", "png"], {"default": "jpeg"}),
                "safety_tolerance": ("INT", {"default": 2, "min": 0, "max": 6}),
                "x_key": ("STRING", {"default": ""}),
            },
            "optional": {
                "seed": ("INT", {"default": -1}),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING")
    FUNCTION = "inpaint"
    CATEGORY = "BFL/Inpainting"

    def inpaint(self, **kwargs):
        try:
            config = BFLConfigLoader()
            
            payload = {
                "image": image_to_base64(kwargs['image']),
                "mask": mask_to_base64(kwargs['mask']),
                "prompt": kwargs['prompt'],
                "steps": kwargs['steps'],
                "guidance": kwargs['guidance'],
                "output_format": kwargs['output_format'],
                "safety_tolerance": kwargs['safety_tolerance'],
                "seed": kwargs['seed'] if kwargs['seed'] != -1 else None,
            }
            
            response = requests.post(
                url="https://api.bfl.ai/v1/flux-pro-1.0-fill",
                headers={"x-key": config.get_api_key(kwargs['x_key']), "Content-Type": "application/json"},
                json={k: v for k, v in payload.items() if v is not None},
                timeout=30
            )
            
            return handle_api_response_with_status(response, kwargs['output_format'], kwargs['x_key'])
        
        except Exception as e:
            error_msg = str(e)
            print(f"BFL Inpainting Error: {error_msg}")
            return (create_error_image(), f"✗ Error: {error_msg}")

class BFL_ImageExpander:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "top": ("INT", {"default": 0, "min": 0, "max": 2048}),
                "bottom": ("INT", {"default": 0, "min": 0, "max": 2048}),
                "left": ("INT", {"default": 0, "min": 0, "max": 2048}),
                "right": ("INT", {"default": 0, "min": 0, "max": 2048}),
                "prompt": ("STRING", {"multiline": True}),
                "steps": ("INT", {"default": 50, "min": 15, "max": 50}),
                "guidance": ("FLOAT", {"default": 60.0, "min": 1.5, "max": 100.0}),
                "output_format": (["jpeg", "png"], {"default": "jpeg"}),
                "safety_tolerance": ("INT", {"default": 2, "min": 0, "max": 6}),
                "x_key": ("STRING", {"default": ""}),
            },
            "optional": {
                "seed": ("INT", {"default": -1}),
                "prompt_upsampling": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING")
    FUNCTION = "expand"
    CATEGORY = "BFL/Expansion"

    def expand(self, **kwargs):
        try:
            config = BFLConfigLoader()
            
            payload = {
                "image": image_to_base64(kwargs['image']),
                "top": kwargs['top'],
                "bottom": kwargs['bottom'],
                "left": kwargs['left'],
                "right": kwargs['right'],
                "prompt": kwargs['prompt'],
                "steps": kwargs['steps'],
                "guidance": kwargs['guidance'],
                "output_format": kwargs['output_format'],
                "safety_tolerance": kwargs['safety_tolerance'],
                "seed": kwargs['seed'] if kwargs['seed'] != -1 else None,
                "prompt_upsampling": kwargs.get('prompt_upsampling', False),
            }
            
            response = requests.post(
                url="https://api.bfl.ai/v1/flux-pro-1.0-expand",
                headers={"x-key": config.get_api_key(kwargs['x_key']), "Content-Type": "application/json"},
                json={k: v for k, v in payload.items() if v is not None},
                timeout=30
            )
            
            return handle_api_response_with_status(response, kwargs['output_format'], kwargs['x_key'])
        
        except Exception as e:
            error_msg = str(e)
            print(f"BFL Expansion Error: {error_msg}")
            return (create_error_image(), f"✗ Error: {error_msg}")

class BFL_FluxKontext:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "model": (["flux-kontext-pro", "flux-kontext-max"], {"default": "flux-kontext-pro"}),
                "output_format": (["jpeg", "png"], {"default": "png"}),
                "safety_tolerance": ("INT", {"default": 2, "min": 0, "max": 6}),
                "x_key": ("STRING", {"default": ""}),
            },
            "optional": {
                "input_image": ("IMAGE",),
                "input_image_2": ("IMAGE",),
                "input_image_3": ("IMAGE",),
                "input_image_4": ("IMAGE",),
                "seed": ("INT", {"default": -1}),
                "aspect_ratio": ("STRING", {"default": ""}),
                "prompt_upsampling": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING")
    FUNCTION = "generate"
    CATEGORY = "BFL/Kontext"

    def generate(self, **kwargs):
        try:
            config = BFLConfigLoader()
            
            payload = {
                "prompt": kwargs['prompt'],
                "output_format": kwargs['output_format'],
                "safety_tolerance": kwargs['safety_tolerance'],
                "seed": kwargs['seed'] if kwargs['seed'] != -1 else None,
                "prompt_upsampling": kwargs.get('prompt_upsampling', False),
            }
            
            # Agregar campos opcionales solo si tienen valor
            if kwargs.get('input_image') is not None:
                payload['input_image'] = image_to_base64(kwargs['input_image'])
            if kwargs.get('input_image_2') is not None:
                payload['input_image_2'] = image_to_base64(kwargs['input_image_2'])
            if kwargs.get('input_image_3') is not None:
                payload['input_image_3'] = image_to_base64(kwargs['input_image_3'])
            if kwargs.get('input_image_4') is not None:
                payload['input_image_4'] = image_to_base64(kwargs['input_image_4'])
            
            if kwargs.get('aspect_ratio') and kwargs['aspect_ratio'].strip():
                payload['aspect_ratio'] = kwargs['aspect_ratio']
            
            response = requests.post(
                url=f"https://api.bfl.ai/v1/{kwargs['model']}",
                headers={"x-key": config.get_api_key(kwargs['x_key']), "Content-Type": "application/json"},
                json={k: v for k, v in payload.items() if v is not None},
                timeout=30
            )
            
            return handle_api_response_with_status(response, kwargs['output_format'], kwargs['x_key'])
        
        except Exception as e:
            error_msg = str(e)
            print(f"BFL Flux Kontext Error: {error_msg}")
            return (create_error_image(), f"✗ Error: {error_msg}")

class BFL_FluxUltra:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "aspect_ratio": ("STRING", {"default": "16:9"}),
                "output_format": (["jpeg", "png"], {"default": "jpeg"}),
                "safety_tolerance": ("INT", {"default": 2, "min": 0, "max": 6}),
                "x_key": ("STRING", {"default": ""}),
            },
            "optional": {
                "seed": ("INT", {"default": -1}),
                "prompt_upsampling": ("BOOLEAN", {"default": False}),
                "raw": ("BOOLEAN", {"default": False}),
                "image_prompt": ("IMAGE",),
                "image_prompt_strength": ("FLOAT", {"default": 0.1, "min": 0.0, "max": 1.0}),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING")
    FUNCTION = "generate"
    CATEGORY = "BFL/Ultra"

    def generate(self, **kwargs):
        try:
            config = BFLConfigLoader()
            
            payload = {
                "prompt": kwargs['prompt'],
                "aspect_ratio": kwargs['aspect_ratio'],
                "output_format": kwargs['output_format'],
                "safety_tolerance": kwargs['safety_tolerance'],
                "seed": kwargs['seed'] if kwargs['seed'] != -1 else None,
                "prompt_upsampling": kwargs.get('prompt_upsampling', False),
                "raw": kwargs.get('raw', False),
            }
            
            # Agregar image_prompt solo si se proporciona
            if kwargs.get('image_prompt') is not None:
                payload['image_prompt'] = image_to_base64(kwargs['image_prompt'])
                payload['image_prompt_strength'] = kwargs.get('image_prompt_strength', 0.1)
            
            response = requests.post(
                url="https://api.bfl.ai/v1/flux-pro-1.1-ultra",
                headers={"x-key": config.get_api_key(kwargs['x_key']), "Content-Type": "application/json"},
                json={k: v for k, v in payload.items() if v is not None},
                timeout=30
            )
            
            return handle_api_response_with_status(response, kwargs['output_format'], kwargs['x_key'])
        
        except Exception as e:
            error_msg = str(e)
            print(f"BFL Flux Ultra Error: {error_msg}")
            return (create_error_image(), f"✗ Error: {error_msg}")

class BFL_Flux2Pro:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "safety_tolerance": ("INT", {"default": 2, "min": 0, "max": 5}),
                "output_format": (["jpeg", "png"], {"default": "jpeg"}),
                "x_key": ("STRING", {"default": ""}),
            },
            "optional": {
                "input_image": ("IMAGE",),
                "input_image_2": ("IMAGE",),
                "input_image_3": ("IMAGE",),
                "input_image_4": ("IMAGE",),
                "input_image_5": ("IMAGE",),
                "input_image_6": ("IMAGE",),
                "input_image_7": ("IMAGE",),
                "input_image_8": ("IMAGE",),
                "seed": ("INT", {"default": -1}),
                "width": ("INT", {"default": 0, "min": 64}),
                "height": ("INT", {"default": 0, "min": 64}),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING")
    FUNCTION = "generate"
    CATEGORY = "BFL/Flux2"

    def generate(self, **kwargs):
        try:
            config = BFLConfigLoader()
            
            payload = {
                "prompt": kwargs['prompt'],
                "safety_tolerance": kwargs['safety_tolerance'],
                "output_format": kwargs['output_format'],
                "seed": kwargs['seed'] if kwargs['seed'] != -1 else None,
            }
            
            # Agregar width y height solo si tienen valor mayor a 0
            if kwargs.get('width', 0) > 0:
                payload['width'] = kwargs['width']
            if kwargs.get('height', 0) > 0:
                payload['height'] = kwargs['height']
            
            # Agregar imágenes de entrada solo si se proporcionan
            if kwargs.get('input_image') is not None:
                payload['input_image'] = image_to_base64(kwargs['input_image'])
            if kwargs.get('input_image_2') is not None:
                payload['input_image_2'] = image_to_base64(kwargs['input_image_2'])
            if kwargs.get('input_image_3') is not None:
                payload['input_image_3'] = image_to_base64(kwargs['input_image_3'])
            if kwargs.get('input_image_4') is not None:
                payload['input_image_4'] = image_to_base64(kwargs['input_image_4'])
            if kwargs.get('input_image_5') is not None:
                payload['input_image_5'] = image_to_base64(kwargs['input_image_5'])
            if kwargs.get('input_image_6') is not None:
                payload['input_image_6'] = image_to_base64(kwargs['input_image_6'])
            if kwargs.get('input_image_7') is not None:
                payload['input_image_7'] = image_to_base64(kwargs['input_image_7'])
            if kwargs.get('input_image_8') is not None:
                payload['input_image_8'] = image_to_base64(kwargs['input_image_8'])
            
            response = requests.post(
                url="https://api.bfl.ai/v1/flux-2-pro",
                headers={"x-key": config.get_api_key(kwargs['x_key']), "Content-Type": "application/json"},
                json={k: v for k, v in payload.items() if v is not None},
                timeout=30
            )
            
            return handle_api_response_with_status(response, kwargs['output_format'], kwargs['x_key'])
        
        except Exception as e:
            error_msg = str(e)
            print(f"BFL Flux 2 Pro Error: {error_msg}")
            return (create_error_image(), f"✗ Error: {error_msg}")

class BFL_Flux2Flex:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "safety_tolerance": ("INT", {"default": 2, "min": 0, "max": 5}),
                "output_format": (["jpeg", "png"], {"default": "jpeg"}),
                "x_key": ("STRING", {"default": ""}),
            },
            "optional": {
                "input_image": ("IMAGE",),
                "input_image_2": ("IMAGE",),
                "input_image_3": ("IMAGE",),
                "input_image_4": ("IMAGE",),
                "input_image_5": ("IMAGE",),
                "input_image_6": ("IMAGE",),
                "input_image_7": ("IMAGE",),
                "input_image_8": ("IMAGE",),
                "input_image_blob_path": ("STRING", {"default": ""}),
                "seed": ("INT", {"default": -1}),
                "width": ("INT", {"default": 0, "min": 64}),
                "height": ("INT", {"default": 0, "min": 64}),
                "guidance": ("FLOAT", {"default": 5.0, "min": 1.5, "max": 10.0}),
                "steps": ("INT", {"default": 50, "min": 1, "max": 50}),
                "prompt_upsampling": ("BOOLEAN", {"default": True}),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING")
    FUNCTION = "generate"
    CATEGORY = "BFL/Flux2"

    def generate(self, **kwargs):
        try:
            config = BFLConfigLoader()
            
            payload = {
                "prompt": kwargs['prompt'],
                "safety_tolerance": kwargs['safety_tolerance'],
                "output_format": kwargs['output_format'],
                "prompt_upsampling": kwargs.get('prompt_upsampling', True),
                "guidance": kwargs.get('guidance', 5.0),
                "steps": kwargs.get('steps', 50),
                "seed": kwargs['seed'] if kwargs['seed'] != -1 else None,
            }
            
            # Agregar width y height solo si tienen valor mayor a 0
            if kwargs.get('width', 0) > 0:
                payload['width'] = kwargs['width']
            if kwargs.get('height', 0) > 0:
                payload['height'] = kwargs['height']
            
            # Agregar input_image_blob_path solo si tiene valor
            if kwargs.get('input_image_blob_path') and kwargs['input_image_blob_path'].strip():
                payload['input_image_blob_path'] = kwargs['input_image_blob_path']
            
            # Agregar imágenes de entrada solo si se proporcionan
            if kwargs.get('input_image') is not None:
                payload['input_image'] = image_to_base64(kwargs['input_image'])
            if kwargs.get('input_image_2') is not None:
                payload['input_image_2'] = image_to_base64(kwargs['input_image_2'])
            if kwargs.get('input_image_3') is not None:
                payload['input_image_3'] = image_to_base64(kwargs['input_image_3'])
            if kwargs.get('input_image_4') is not None:
                payload['input_image_4'] = image_to_base64(kwargs['input_image_4'])
            if kwargs.get('input_image_5') is not None:
                payload['input_image_5'] = image_to_base64(kwargs['input_image_5'])
            if kwargs.get('input_image_6') is not None:
                payload['input_image_6'] = image_to_base64(kwargs['input_image_6'])
            if kwargs.get('input_image_7') is not None:
                payload['input_image_7'] = image_to_base64(kwargs['input_image_7'])
            if kwargs.get('input_image_8') is not None:
                payload['input_image_8'] = image_to_base64(kwargs['input_image_8'])
            
            response = requests.post(
                url="https://api.bfl.ai/v1/flux-2-flex",
                headers={"x-key": config.get_api_key(kwargs['x_key']), "Content-Type": "application/json"},
                json={k: v for k, v in payload.items() if v is not None},
                timeout=30
            )
            
            return handle_api_response_with_status(response, kwargs['output_format'], kwargs['x_key'])
        
        except Exception as e:
            error_msg = str(e)
            print(f"BFL Flux 2 Flex Error: {error_msg}")
            return (create_error_image(), f"✗ Error: {error_msg}")

NODE_CLASS_MAPPINGS = {
    "BFL Image Generator": BFL_ImageGenerator,
    "BFL Inpainting": BFL_Inpainting,
    "BFL Image Expander": BFL_ImageExpander,
    "BFL Flux Kontext": BFL_FluxKontext,
    "BFL Flux Ultra": BFL_FluxUltra,
    "BFL Flux 2 Pro": BFL_Flux2Pro,
    "BFL Flux 2 Flex": BFL_Flux2Flex,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BFL Image Generator": "BFL Image Generator (Pro 1.1/1.0)",
    "BFL Inpainting": "BFL Inpainting (Pro 1.0 Fill)",
    "BFL Image Expander": "BFL Image Expander (Pro 1.0)",
    "BFL Flux Kontext": "BFL Flux Kontext (Pro/Max)",
    "BFL Flux Ultra": "BFL Flux Ultra (Pro 1.1)",
    "BFL Flux 2 Pro": "BFL Flux 2 Pro",
    "BFL Flux 2 Flex": "BFL Flux 2 Flex",
}
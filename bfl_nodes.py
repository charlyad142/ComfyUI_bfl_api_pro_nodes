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
                "api_version": (["1.1", "1.0"], {"default": "1.1"}),
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
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "BFL/Generation"

    def generate(self, **kwargs):
        try:
            config = BFLConfigLoader()
            endpoint = "flux-pro-1.1" if kwargs['api_version'] == "1.1" else "flux-pro"
            
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
                url=f"https://api.us1.bfl.ai/v1/{endpoint}",
                headers={"x-key": config.get_api_key(kwargs['x_key']), "Content-Type": "application/json"},
                json={k: v for k, v in payload.items() if v is not None},
                timeout=30
            )
            
            return (handle_api_response(response, kwargs['output_format'], kwargs['x_key']),)
        
        except Exception as e:
            print(f"BFL Generation Error: {str(e)}")
            return (create_error_image(),)

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
    
    RETURN_TYPES = ("IMAGE",)
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
                url="https://api.us1.bfl.ai/v1/flux-pro-1.0-fill",
                headers={"x-key": config.get_api_key(kwargs['x_key']), "Content-Type": "application/json"},
                json={k: v for k, v in payload.items() if v is not None},
                timeout=30
            )
            
            return (handle_api_response(response, kwargs['output_format'], kwargs['x_key']),)
        
        except Exception as e:
            print(f"BFL Inpainting Error: {str(e)}")
            return (create_error_image(),)

class BFL_CannyControl:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "control_image": ("IMAGE",),
                "canny_low": ("INT", {"default": 50, "min": 0, "max": 500}),
                "canny_high": ("INT", {"default": 200, "min": 0, "max": 500}),
                "steps": ("INT", {"default": 50, "min": 15, "max": 50}),
                "guidance": ("FLOAT", {"default": 30.0, "min": 1.0, "max": 100.0}),
                "output_format": (["jpeg", "png"], {"default": "jpeg"}),
                "safety_tolerance": ("INT", {"default": 2, "min": 0, "max": 6}),
                "x_key": ("STRING", {"default": ""}),
            },
            "optional": {
                "preprocessed_image": ("IMAGE",),
                "seed": ("INT", {"default": -1}),
                "prompt_upsampling": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "BFL/ControlNet"

    def generate(self, **kwargs):
        try:
            config = BFLConfigLoader()
            
            payload = {
                "prompt": kwargs['prompt'],
                "control_image": image_to_base64(kwargs['control_image']),
                "canny_low_threshold": kwargs['canny_low'],
                "canny_high_threshold": kwargs['canny_high'],
                "steps": kwargs['steps'],
                "guidance": kwargs['guidance'],
                "output_format": kwargs['output_format'],
                "safety_tolerance": kwargs['safety_tolerance'],
                "seed": kwargs['seed'] if kwargs['seed'] != -1 else None,
                "prompt_upsampling": kwargs.get('prompt_upsampling', False),
            }
            
            if kwargs.get('preprocessed_image'):
                payload['preprocessed_image'] = image_to_base64(kwargs['preprocessed_image'])
            
            response = requests.post(
                url="https://api.us1.bfl.ai/v1/flux-pro-1.0-canny",
                headers={"x-key": config.get_api_key(kwargs['x_key']), "Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            
            return (handle_api_response(response, kwargs['output_format'], kwargs['x_key']),)
        
        except Exception as e:
            print(f"BFL Canny Error: {str(e)}")
            return (create_error_image(),)

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
    
    RETURN_TYPES = ("IMAGE",)
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
                url="https://api.us1.bfl.ai/v1/flux-pro-1.0-expand",
                headers={"x-key": config.get_api_key(kwargs['x_key']), "Content-Type": "application/json"},
                json={k: v for k, v in payload.items() if v is not None},
                timeout=30
            )
            
            return (handle_api_response(response, kwargs['output_format'], kwargs['x_key']),)
        
        except Exception as e:
            print(f"BFL Expansion Error: {str(e)}")
            return (create_error_image(),)

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
                "seed": ("INT", {"default": -1}),
                "aspect_ratio": ("STRING", {"default": ""}),
                "prompt_upsampling": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
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
            
            if kwargs.get('aspect_ratio') and kwargs['aspect_ratio'].strip():
                payload['aspect_ratio'] = kwargs['aspect_ratio']
            
            response = requests.post(
                url=f"https://api.us1.bfl.ai/v1/{kwargs['model']}",
                headers={"x-key": config.get_api_key(kwargs['x_key']), "Content-Type": "application/json"},
                json={k: v for k, v in payload.items() if v is not None},
                timeout=30
            )
            
            return (handle_api_response(response, kwargs['output_format'], kwargs['x_key']),)
        
        except Exception as e:
            print(f"BFL Flux Kontext Error: {str(e)}")
            return (create_error_image(),)

class BFL_DepthControl:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "control_image": ("IMAGE",),
                "steps": ("INT", {"default": 50, "min": 15, "max": 50}),
                "guidance": ("FLOAT", {"default": 15.0, "min": 1.0, "max": 100.0}),
                "output_format": (["jpeg", "png"], {"default": "jpeg"}),
                "safety_tolerance": ("INT", {"default": 2, "min": 0, "max": 6}),
                "x_key": ("STRING", {"default": ""}),
            },
            "optional": {
                "preprocessed_image": ("IMAGE",),
                "seed": ("INT", {"default": -1}),
                "prompt_upsampling": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "BFL/ControlNet"

    def generate(self, **kwargs):
        try:
            config = BFLConfigLoader()
            
            payload = {
                "prompt": kwargs['prompt'],
                "control_image": image_to_base64(kwargs['control_image']),
                "steps": kwargs['steps'],
                "guidance": kwargs['guidance'],
                "output_format": kwargs['output_format'],
                "safety_tolerance": kwargs['safety_tolerance'],
                "seed": kwargs['seed'] if kwargs['seed'] != -1 else None,
                "prompt_upsampling": kwargs.get('prompt_upsampling', False),
            }
            
            if kwargs.get('preprocessed_image'):
                payload['preprocessed_image'] = image_to_base64(kwargs['preprocessed_image'])
            
            response = requests.post(
                url="https://api.us1.bfl.ai/v1/flux-pro-1.0-depth",
                headers={"x-key": config.get_api_key(kwargs['x_key']), "Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            
            return (handle_api_response(response, kwargs['output_format'], kwargs['x_key']),)
        
        except Exception as e:
            print(f"BFL Depth Error: {str(e)}")
            return (create_error_image(),)

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
    
    RETURN_TYPES = ("IMAGE",)
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
                url="https://api.us1.bfl.ai/v1/flux-pro-1.1-ultra",
                headers={"x-key": config.get_api_key(kwargs['x_key']), "Content-Type": "application/json"},
                json={k: v for k, v in payload.items() if v is not None},
                timeout=30
            )
            
            return (handle_api_response(response, kwargs['output_format'], kwargs['x_key']),)
        
        except Exception as e:
            print(f"BFL Flux Ultra Error: {str(e)}")
            return (create_error_image(),)

NODE_CLASS_MAPPINGS = {
    "BFL Image Generator": BFL_ImageGenerator,
    "BFL Inpainting": BFL_Inpainting,
    "BFL Canny Control": BFL_CannyControl,
    "BFL Image Expander": BFL_ImageExpander,
    "BFL Flux Kontext": BFL_FluxKontext,
    "BFL Depth Control": BFL_DepthControl,
    "BFL Flux Ultra": BFL_FluxUltra,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BFL Image Generator": "BFL Image Generator (Pro 1.1/1.0)",
    "BFL Inpainting": "BFL Inpainting (Pro 1.0 Fill)",
    "BFL Canny Control": "BFL Canny Control (Pro 1.0)",
    "BFL Image Expander": "BFL Image Expander (Pro 1.0)",
    "BFL Flux Kontext": "BFL Flux Kontext (Pro/Max)",
    "BFL Depth Control": "BFL Depth Control (Pro 1.0)",
    "BFL Flux Ultra": "BFL Flux Ultra (Pro 1.1)",
}
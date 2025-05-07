import os
import base64
import requests
import numpy as np
from PIL import Image
import io
import torch
import configparser
import time
from urllib.parse import urljoin

class BFLConfigLoader:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.load_config()
        return cls._instance
    
    def load_config(self):
        self.config = configparser.ConfigParser()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "config.ini")
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found at {config_path}")
            
        self.config.read(config_path)
        
    @property
    def api_key(self):
        key = self.config.get('API', 'X_KEY', fallback=None)
        if not key:
            raise ValueError("X_KEY not found in config.ini")
        return key

def image_to_base64(image_tensor, format='PNG'):
    image = Image.fromarray((image_tensor.numpy().squeeze() * 255).astype(np.uint8))
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def mask_to_base64(mask_tensor, format='PNG'):
    mask_array = (mask_tensor.numpy().squeeze() * 255).astype(np.uint8)
    mask_image = Image.fromarray(mask_array)
    buffered = io.BytesIO()
    mask_image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def handle_api_response(response, output_format):
    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")
    
    result = response.json()
    
    if 'id' not in result:
        raise Exception("Invalid API response format")
    
    return poll_task_result(result['id'], output_format)

def poll_task_result(task_id, output_format, max_attempts=15):
    config = BFLConfigLoader()
    base_url = "https://api.us1.bfl.ai/v1/"
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(
                urljoin(base_url, f"get_result?id={task_id}"),
                headers={"x-key": config.api_key},
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'Ready':
                img_response = requests.get(data['result']['sample'])
                img = Image.open(io.BytesIO(img_response.content))
                
                with io.BytesIO() as buffer:
                    img.save(buffer, format=output_format.upper())
                    buffer.seek(0)
                    img_array = np.array(Image.open(buffer)).astype(np.float32) / 255.0
                    return torch.from_numpy(img_array)[None,]
            
            time.sleep(2 ** attempt + 5)
        
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            continue
    
    raise Exception("Max polling attempts reached")

def create_error_image():
    blank = Image.new('RGB', (512, 512), color='red')
    blank.putpixel((256, 256), (255, 0, 0))
    tensor = torch.from_numpy(np.array(blank).astype(np.float32) / 255.0)
    return tensor[None,]
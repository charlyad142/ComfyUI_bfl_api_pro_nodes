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
        
        if os.path.exists(config_path):
            self.config.read(config_path)
    
    def get_api_key(self, node_api_key=None):
        # Primero intentar obtener la key del archivo config.ini
        try:
            if self.config.has_section('API') and self.config.has_option('API', 'X_KEY'):
                return self.config.get('API', 'X_KEY')
        except:
            pass
            
        # Si no hay key en config.ini o hay error, usar la key del nodo
        if node_api_key and node_api_key.strip():
            return node_api_key
            
        # Si no hay key en ningún lado, lanzar error
        raise ValueError("No se encontró una API key válida. Por favor, configure una API key en el nodo o en el archivo config.ini")

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

def handle_api_response(response, output_format, node_api_key=None):
    # Manejar diferentes códigos de estado HTTP
    if response.status_code == 200:
        try:
            result = response.json()
            
            if 'id' not in result:
                raise Exception("Invalid API response format: missing task ID")
            
            return poll_task_result(result['id'], output_format, node_api_key=node_api_key)
            
        except ValueError as e:
            raise Exception(f"Invalid JSON response from API: {str(e)}")
    
    elif response.status_code == 422:
        try:
            error_data = response.json()
            detail = error_data.get('detail', 'Unknown validation error')
            if isinstance(detail, list) and len(detail) > 0:
                error_msg = detail[0].get('msg', 'Validation error')
            else:
                error_msg = str(detail)
            raise Exception(f"Validation Error: {error_msg}")
        except ValueError:
            raise Exception(f"Validation Error: {response.text}")
    
    elif response.status_code == 401:
        raise Exception("Unauthorized: Please check your API key")
    
    elif response.status_code == 403:
        raise Exception("Forbidden: Insufficient permissions or quota exceeded")
    
    elif response.status_code == 429:
        raise Exception("Rate limit exceeded: Please wait before making another request")
    
    elif response.status_code >= 500:
        raise Exception(f"Server Error ({response.status_code}): Please try again later")
    
    else:
        try:
            error_data = response.json()
            error_msg = error_data.get('error', error_data.get('message', response.text))
        except ValueError:
            error_msg = response.text
        
        raise Exception(f"API Error {response.status_code}: {error_msg}")

def poll_task_result(task_id, output_format, max_attempts=10, node_api_key=None):
    config = BFLConfigLoader()
    base_url = "https://api.us1.bfl.ai/v1/"
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(
                urljoin(base_url, f"get_result?id={task_id}"),
                headers={"x-key": config.get_api_key(node_api_key)},
                timeout=30
            )
            
            # Manejar errores HTTP
            if response.status_code == 422:
                error_data = response.json()
                raise Exception(f"Validation Error: {error_data.get('detail', 'Unknown validation error')}")
            
            response.raise_for_status()
            data = response.json()
            
            # Verificar que tenemos los campos requeridos
            if 'status' not in data:
                raise Exception("Invalid API response: missing status field")
            
            status = data['status']
            
            # Manejar diferentes estados según la documentación
            if status == 'Ready':
                if 'result' not in data or not data['result'] or 'sample' not in data['result']:
                    raise Exception("Task completed but no result available")
                
                img_response = requests.get(data['result']['sample'])
                img_response.raise_for_status()
                img = Image.open(io.BytesIO(img_response.content))
                
                with io.BytesIO() as buffer:
                    img.save(buffer, format=output_format.upper())
                    buffer.seek(0)
                    img_array = np.array(Image.open(buffer)).astype(np.float32) / 255.0
                    return torch.from_numpy(img_array)[None,]
            
            elif status == 'Error':
                error_msg = "Task failed"
                if 'details' in data and data['details']:
                    error_msg = f"Task failed: {data['details']}"
                raise Exception(error_msg)
            
            elif status == 'Task not found':
                raise Exception(f"Task not found: {task_id}")
            
            elif status == 'Request Moderated':
                raise Exception("Request was moderated by content filters")
            
            elif status == 'Content Moderated':
                raise Exception("Generated content was moderated by safety filters")
            
            elif status == 'Pending':
                # Tarea en progreso, continuar polling
                progress = data.get('progress', 0)
                print(f"Task {task_id} in progress: {progress}% (attempt {attempt + 1}/{max_attempts})")
                
                # Tiempo de espera más razonable: máximo 60 segundos por intento
                wait_time = min(2 ** attempt + 5, 60)
                time.sleep(wait_time)
                continue
            
            else:
                # Estado desconocido
                print(f"Unknown status '{status}' for task {task_id}, retrying...")
                wait_time = min(2 ** attempt + 5, 60)
                time.sleep(wait_time)
                continue
        
        except requests.exceptions.Timeout:
            print(f"Timeout on attempt {attempt + 1}/{max_attempts} for task {task_id}")
            if attempt == max_attempts - 1:
                raise Exception(f"Request timeout after {max_attempts} attempts")
            wait_time = min(2 ** attempt + 5, 60)
            time.sleep(wait_time)
            continue
        
        except requests.exceptions.RequestException as e:
            print(f"Request error on attempt {attempt + 1}/{max_attempts}: {str(e)}")
            if attempt == max_attempts - 1:
                raise Exception(f"Request failed after {max_attempts} attempts: {str(e)}")
            wait_time = min(2 ** attempt + 5, 60)
            time.sleep(wait_time)
            continue
        
        except Exception as e:
            # Para otros errores (parsing JSON, etc.), lanzar inmediatamente
            raise Exception(f"Error processing task {task_id}: {str(e)}")
    
    raise Exception(f"Max polling attempts ({max_attempts}) reached for task {task_id}")

def create_error_image():
    blank = Image.new('RGB', (512, 512), color='red')
    blank.putpixel((256, 256), (255, 0, 0))
    tensor = torch.from_numpy(np.array(blank).astype(np.float32) / 255.0)
    return tensor[None,]
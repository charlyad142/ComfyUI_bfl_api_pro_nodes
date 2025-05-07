# ComfyUI BFL API Pro Nodes

Este nodo personalizado para ComfyUI proporciona integración con la API de BFL (Black Forest Labs) para mejorar y optimizar el procesamiento de imágenes. Permite utilizar Flux Pro, directamente dentro de ComfyUI, ofreciendo capacidades avanzadas de procesamiento de imágenes.

## Características

- Integración con la API de BFL
- Procesamiento de imágenes optimizado
- Compatible con el flujo de trabajo de ComfyUI

## Instalación

1. Navega a la carpeta `custom_nodes` de tu instalación de ComfyUI
2. Clona este repositorio:
```bash
git clone https://github.com/charlyad142/ComfyUI_bfl_api_pro_nodes.git
```
3. Reinicia ComfyUI

## Configuración

Para utilizar este nodo, necesitas configurar tu API key de BFL. Sigue estos pasos:

1. Crea un archivo `config.ini` en la raíz del nodo
2. Agrega la siguiente configuración:

```ini
[API]
X_KEY = tu_api_key_aquí
```

### Obtención de API Key

1. Regístrate en [BFL Platform](https://auth.bfl.ai/)
2. Ve a tu panel de control
3. En la sección de API Keys, genera una nueva key
4. Copia la key y pégala en tu archivo `config.ini`

## Uso

1. En ComfyUI, busca los nodos "BFL" en el menú de nodos
2. Arrastra el nodo deseado a tu flujo de trabajo
3. Conecta los nodos según tus necesidades

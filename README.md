# ComfyUI BFL API Pro Nodes

Este nodo personalizado para ComfyUI proporciona integración con la API de BFL (Bing Face Library) para mejorar y optimizar el procesamiento de imágenes.

## Características

- Integración con la API de BFL
- Procesamiento de imágenes optimizado
- Funciones avanzadas de manipulación facial
- Compatible con el flujo de trabajo de ComfyUI

## Instalación

1. Navega a la carpeta `custom_nodes` de tu instalación de ComfyUI
2. Clona este repositorio:
```bash
git clone https://github.com/tu-usuario/ComfyUI_bfl_api_pro_nodes.git
```
3. Reinicia ComfyUI

## Configuración

Para utilizar este nodo, necesitas configurar tu API key de BFL. Sigue estos pasos:

1. Crea un archivo `config.ini` en la raíz del nodo
2. Agrega la siguiente configuración:

```ini
[API]
api_key = tu_api_key_aquí
```

### Obtención de API Key

1. Regístrate en [BFL Platform](https://bfl-platform.com)
2. Ve a tu panel de control
3. En la sección de API Keys, genera una nueva key
4. Copia la key y pégala en tu archivo `config.ini`

## Uso

1. En ComfyUI, busca los nodos "BFL" en el menú de nodos
2. Arrastra el nodo deseado a tu flujo de trabajo
3. Conecta los nodos según tus necesidades

## Nodos Disponibles

- **BFL Face Detection**: Detecta rostros en las imágenes
- **BFL Face Enhancement**: Mejora la calidad de los rostros detectados
- **BFL Face Swap**: Permite intercambiar rostros entre imágenes

## Soporte

Si encuentras algún problema o tienes preguntas:
- Abre un issue en este repositorio
- Contacta al soporte de BFL

## Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles. 
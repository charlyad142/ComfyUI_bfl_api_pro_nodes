# ComfyUI BFL API Pro Nodes

Este nodo personalizado para ComfyUI proporciona integración completa con la API de BFL (Black Forest Labs) para mejorar y optimizar el procesamiento de imágenes. Permite utilizar todos los modelos de Flux Pro, Flux Kontext y Flux Ultra directamente dentro de ComfyUI, ofreciendo capacidades avanzadas de procesamiento de imágenes.

## Características

- ✅ **Integración completa con la API de BFL**
- ✅ **Múltiples modelos soportados**: Flux Pro, Flux Kontext, Flux Ultra
- ✅ **ControlNet avanzado**: Canny, Depth
- ✅ **Inpainting y expansión de imágenes**
- ✅ **Sistema flexible de API keys** con prioridad automática
- ✅ **Procesamiento de imágenes optimizado**
- ✅ **Compatible con el flujo de trabajo de ComfyUI**
- ✅ **Manejo robusto de errores**

## Nodos Disponibles

### 🎨 Generación de Imágenes
- **BFL Image Generator (Pro 1.1/1.0)**: Generación básica de imágenes con soporte para versiones 1.0 y 1.1
- **BFL Flux Ultra (Pro 1.1)**: Modelo Ultra para máxima calidad

### 🎭 ControlNet
- **BFL Canny Control (Pro 1.0)**: Control de bordes con detección Canny
- **BFL Depth Control (Pro 1.0)**: Control de profundidad

### 🔧 Edición y Manipulación
- **BFL Inpainting (Pro 1.0 Fill)**: Rellenado inteligente de áreas
- **BFL Image Expander (Pro 1.0)**: Expansión de imágenes con IA

### 🌟 Modelos Especializados
- **BFL Flux Kontext (Pro/Max)**: Modelos Kontext Pro y Max para casos especiales

## Instalación

1. Navega a la carpeta `custom_nodes` de tu instalación de ComfyUI
2. Clona este repositorio:
```bash
git clone https://github.com/charlyad142/ComfyUI_bfl_api_pro_nodes.git
```
3. Reinicia ComfyUI

## Configuración de API Key

### Opción 1: Archivo config.ini (Recomendado)
1. Crea un archivo `config.ini` en la raíz del nodo
2. Agrega la siguiente configuración:

```ini
[API]
X_KEY = tu_api_key_aquí
```

### Opción 2: Campo x_key en cada nodo
- Cada nodo tiene un campo `x_key` donde puedes ingresar tu API key directamente
- Útil para usar diferentes keys en diferentes nodos

### Sistema de Prioridad de API Keys
El sistema busca la API key en el siguiente orden:
1. **Archivo config.ini** (prioridad más alta)
2. **Campo x_key del nodo** (si config.ini no existe o no tiene key)
3. **Error** (si no hay key en ningún lado)

### Obtención de API Key

1. Regístrate en [BFL Platform](https://auth.bfl.ai/)
2. Ve a tu panel de control
3. En la sección de API Keys, genera una nueva key
4. Copia la key y pégala en tu archivo `config.ini` o en el campo `x_key` del nodo

## Uso

### Básico
1. En ComfyUI, busca los nodos "BFL" en el menú de nodos
2. Arrastra el nodo deseado a tu flujo de trabajo
3. Configura tu API key (en config.ini o en el campo x_key)
4. Conecta los nodos según tus necesidades

### Ejemplos de Uso

#### Generación de Imágenes
```
BFL Image Generator → Prompt → Output
```

#### ControlNet con Canny
```
Input Image → BFL Canny Control → Output
```

#### Inpainting
```
Image + Mask → BFL Inpainting → Output
```

#### Expansión de Imágenes
```
Image → BFL Image Expander → Output
```

## Parámetros Comunes

### Campos Requeridos
- **prompt**: Descripción de la imagen a generar
- **x_key**: Tu API key de BFL
- **output_format**: Formato de salida (jpeg/png)
- **safety_tolerance**: Tolerancia de seguridad (0-6)

### Campos Opcionales
- **seed**: Semilla para reproducibilidad (-1 para aleatorio)
- **steps**: Número de pasos de generación (15-50)
- **guidance**: Guía de generación (1.0-100.0)

## Modelos Específicos

### Flux Pro 1.1/1.0
- **Versión 1.1**: Sin parámetros de steps/guidance
- **Versión 1.0**: Con parámetros de steps/guidance

### Flux Ultra
- **Aspect Ratio**: Control de relación de aspecto
- **Raw Mode**: Modo raw para mayor control
- **Image Prompt**: Soporte para imágenes de referencia

### Flux Kontext
- **Pro/Max**: Dos modelos especializados
- **Aspect Ratio**: Control de relación de aspecto

### ControlNet
- **Canny**: Detección de bordes con umbrales configurables
- **Depth**: Control de profundidad

## Solución de Problemas

### Error de API Key
```
"No se encontró una API key válida. Por favor, configure una API key en el nodo o en el archivo config.ini"
```
**Solución**: Verifica que tu API key esté configurada correctamente en config.ini o en el campo x_key del nodo.

### Error de Conexión
```
"API Error 401: Unauthorized"
```
**Solución**: Verifica que tu API key sea válida y tenga créditos disponibles.

### Error de Formato
```
"Invalid API response format"
```
**Solución**: Verifica que todos los parámetros requeridos estén configurados correctamente.

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte técnico o preguntas:
- Abre un issue en GitHub
- Consulta la documentación de BFL: [BFL Platform](https://auth.bfl.ai/)

## Changelog

### v2.0.0
- ✅ Agregado soporte para Flux Ultra
- ✅ Agregado nodo de Depth Control
- ✅ Agregado nodo de Flux Kontext
- ✅ Sistema flexible de API keys con prioridad automática
- ✅ Mejorado el manejo de errores
- ✅ Eliminados campos de webhook innecesarios

### v1.0.0
- ✅ Nodos básicos de generación, inpainting y control
- ✅ Soporte para config.ini
- ✅ Integración con ComfyUI


# SocialStarter ![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Django](https://img.shields.io/badge/Django-3.2-green) ![django-allauth](https://img.shields.io/badge/django--allauth-0.45-orange)


SocialStarter es un proyecto de código abierto diseñado para servir como plantilla
para la creación de redes sociales. Incluye características esenciales como publicaciones,
likes, comentarios, relaciones entre usuarios y autenticación, utilizando Django y django-allauth.
Ideal para desarrolladores que buscan un punto de partida sólido para sus proyectos sociales.


## 🌟 Características

- 📝 Publicaciones de texto, imágenes y videos
- ❤️ Sistema de likes y comentarios
- 👥 Relaciones de seguimiento entre usuarios (followers/following)
- 🚀 Perfiles de usuario extendidos
- 🔒 Autenticación y registro de usuarios con `django-allauth` (incluye soporte para autenticación social)

## 🛠 Tecnologías Utilizadas

- Django
- django-allauth
- PostgreSQL (u otra base de datos de tu elección)
- Django Rest Framework (si aplica)
- Tailwind CSS (si aplica)

## ⚙️ Requisitos Previos

Asegúrate de tener instalado Python 3.8+, Pip y Virtualenv, además de una instancia de PostgreSQL (o la base de datos que prefieras) corriendo si decides utilizarla.

## 🚀 Configuración del Proyecto

### 📦 Clonar el Repositorio

```
git clone https://tu-repositorio-aqui.git
cd nombre-del-proyecto
```

### 🌐 Configurar el Entorno Virtual

```
python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
```

### 📚 Instalar Dependencias

```
pip install -r requirements.txt
```

### 🔑 Configurar Variables de Entorno

Crea un archivo `.env` en el directorio principal del proyecto y agrega las siguientes variables de entorno:

```
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True  # Cambiar a False en producción
DATABASE_URL=URL_de_tu_base_de_datos
ALLOWED_HOSTS=.localhost, .tu-dominio.com
```

### 🗃 Migraciones y Crear Superusuario

```
python manage.py migrate
python manage.py createsuperuser
```

### 🏃‍♂️ Ejecutar el Proyecto

```
python manage.py runserver
```

El servidor de desarrollo iniciará en `http://127.0.0.1:8000/`.

## 🔐 Uso de django-allauth

Para configurar `django-allauth` y habilitar la autenticación social, sigue la [documentación oficial de django-allauth](https://django-allauth.readthedocs.io/).

## 🤝 Cómo Contribuir

Si deseas contribuir al proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu característica (`git checkout -b mi-nueva-característica`).
3. Haz tus cambios y commit (`git commit -am 'Añadir alguna característica'`).
4. Push a la rama (`git push origin mi-nueva-característica`).
5. Crea una nueva Pull Request.


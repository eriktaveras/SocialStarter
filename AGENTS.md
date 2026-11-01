# AGENTS.md · SocialStarter

SocialStarter es una plantilla open source (MIT) de red social hecha con Django. Trae usuarios con avatar y portada (allauth), posts, feed, seguidores (relationship), likes y comentarios (interactions), mensajes directos, notificaciones en tiempo real por WebSocket y una app de ajustes de usuario con API DRF. Es un proyecto monolítico con varias apps Django, sin CI y sin tests reales.

## Stack

Python 3 + Django 5.0.1 (requirements.txt fija 5.0.1, aunque el README dice 5.2), django-allauth 0.60, Django Channels 4 + channels-redis + daphne (WebSockets), Django REST Framework, Pillow; frontend

## Comandos

- Instalar: `uv venv --python 3.12 && uv pip install -r requirements.txt djangorestframework && printf 'SECRET_KEY=dev-only-key\nDEBUG=True\n' > .env && uv run python manage.py migrate`
- Tests: `uv run python manage.py test`
- Build: `uv run python manage.py check`

## Notas para agentes

Es un proyecto Django: el punto de entrada es manage.py y la configuración está en main/settings.py (también main/urls.py y main/asgi.py). Hay una app por carpeta: users, posts, feed, relationship, interactions, messaging, notifications, settings y user_notifications. user_notifications no está en INSTALLED_APPS y parece código muerto. Los tests van en <app>/tests.py; hoy todos están vacíos, así que si añades tests usa django.test.TestCase. No hay CI, ni AGENTS.md o CLAUDE.md, ni CONTRIBUTING, ni linter configurado. Tampoco hay pyproject.toml, aunque el README hable de Poetry. Las plantillas globales están en templates/ y las de allauth en templates/account. settings.py lee SECRET_KEY, DEBUG y EMAIL_* de .env con python-dotenv. Sin SECRET_KEY, Django no arranca. Si cambias modelos, genera las migraciones con makemigrations y no edites las ya existentes. No ejecutes check_db.py ni fix_db.py: son scripts sueltos que tocan db.sqlite3 directamente con sqlite3. La app 'settings' se llama igual que un módulo de configuración; no la renombres. Para el runtime de Channels hace falta Redis en 127.0.0.1:6379; para manage.py test y check no.

---
Propuesto por el Taller de hermes-web a partir de su reconocimiento del repo; revísalo antes de hacer merge.

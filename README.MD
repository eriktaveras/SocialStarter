# SocialStarter ![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Django](https://img.shields.io/badge/Django-5.2-green) ![django-allauth](https://img.shields.io/badge/django--allauth-0.45-orange) ![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)

![SocialStarter Screenshot](https://github.com/eriktaveras/SocialStarter/assets/10116703/88b2465a-9cd8-42df-813d-2c9aad9991f7)

SocialStarter is an open-source project designed to serve as a complete template for building modern social networks. It includes all essential features needed for a social platform, utilizing Django and a modern technology stack. This project is ideal for developers looking for a solid foundation to build upon, or for educational purposes to understand how social networks function under the hood.

## 🌟 Features

### User Management
- 🔒 Complete authentication system with django-allauth
- 👤 Extended user profiles with customizable fields
- 🖼️ Profile pictures and cover images
- 📱 Responsive UI for mobile and desktop
- 🔐 Password reset and account management

### Content & Posts
- 📝 Text, image, and video posts
- 📊 News feed with algorithmic sorting
- 🔄 Repost/share functionality
- 📎 Attachment support
- 🏷️ Tagging and mentions

### Interactions
- ❤️ Like and comment system
- 📣 Nested comments and replies
- 👍 Reaction system (like, love, etc.)
- 💬 Rich text formatting in comments

### Social Connections
- 👥 User follow relationships (followers/following)
- 🔔 Friend/follow requests
- 🚫 Block and mute functionality
- 👁️ Privacy controls for content visibility

### Messaging
- 💌 Direct messaging between users
- 📨 Inbox and conversation management
- 👾 Emoji support in messages
- 🔄 Real-time messaging with WebSockets

### Notifications
- 🔔 Real-time notifications
- 📧 Email notifications
- 🔕 Notification preferences
- 📱 Push notification framework

### Settings & Privacy
- ⚙️ Comprehensive user settings
- 🔒 Privacy controls
- 🌙 Theme customization (dark/light mode)
- 🌐 Language preferences

### Admin Features
- 🔧 Admin dashboard
- 📊 User and content management
- 📈 Basic analytics
- 🚫 Moderation tools

## 🛠 Technologies Used

- **Backend**: Django 5.2, Python 3.8+
- **Authentication**: django-allauth
- **Real-time Features**: Django Channels, WebSockets
- **Frontend**: Tailwind CSS, AlpineJS
- **Database**: SQLite (development), PostgreSQL (recommended for production)
- **API**: Django REST Framework
- **Media Storage**: Django File Storage (configurable for cloud storage)

## ⚙️ Prerequisites

- Python 3.8 or higher
- Pip package manager
- Virtual environment tool (virtualenv or poetry)
- Git
- (Optional) PostgreSQL for production deployments

## 🚀 Project Setup

### 📦 Clone the Repository

```bash
git clone https://github.com/eriktaveras/SocialStarter.git
cd SocialStarter
```

### 🌐 Set Up Virtual Environment

#### Using Virtualenv
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

#### Using Poetry
```bash
poetry install
poetry shell
```

### 📚 Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔑 Configure Environment Variables

Create a `.env` file in the main project directory with the following:

```plaintext
SECRET_KEY=your_secret_key_here
DEBUG=True  # Set to False in production
DATABASE_URL=your_database_url_if_using_postgres
ALLOWED_HOSTS=.localhost, .your-domain.com
EMAIL_HOST=your_email_host
EMAIL_PORT=your_email_port
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email_user
EMAIL_HOST_PASSWORD=your_email_password
```

### 🗃 Setup Database and Create Admin User

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 🏃 Run the Development Server

```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory, covering:
- Detailed setup instructions
- Architecture overview
- Customization guide
- Deployment recommendations
- API documentation (if applicable)

## 🤝 Contributing to SocialStarter

SocialStarter is an **open source project** and welcomes contributions from the community. Here's how you can contribute:

1. **Fork the repository** - Create your own copy of the project
2. **Create a feature branch** - `git checkout -b feature/amazing-feature`
3. **Commit your changes** - `git commit -m 'Add some amazing feature'`
4. **Push to your branch** - `git push origin feature/amazing-feature`
5. **Open a Pull Request** - Go to the original repository and create a PR

### Contribution Guidelines
- Follow the code style of the project
- Write tests for your features when applicable
- Keep pull requests focused on a single feature/fix
- Document your code and any new functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

Erik Taveras - [Website](https://www.eriktaveras.com) - [GitHub](https://github.com/eriktaveras)

Project Link: [https://github.com/eriktaveras/SocialStarter](https://github.com/eriktaveras/SocialStarter)

---

⭐ If you find this project useful, please consider giving it a star on GitHub!

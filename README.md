# VocabMaster - SAT Vocabulary Flash Cards

A modern web application to master SAT vocabulary with 3500+ words, interactive flashcards, and bilingual support (English/Urdu).

## Features

- 🎯 **3500+ SAT Words** - Complete Barron's vocabulary database
- 🔄 **Interactive Flashcards** - Double-click to flip and reveal meanings
- 🔍 **Smart Search** - Search across words, meanings, and examples
- 📱 **Responsive Design** - Works on all devices
- 🌐 **Bilingual Support** - English and Urdu meanings
- 👤 **User Authentication** - Email and Google OAuth login
- 📊 **Progress Tracking** - Monitor your learning journey
- 🎨 **Modern UI** - Clean, professional interface

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/vocabulary-flash-card.git
cd vocabulary-flash-card
```

### 2. Setup Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
```

### 3. Configure Database
```bash
# Run migrations
python manage.py migrate

# Load vocabulary data
python add_comprehensive_data.py

# Create admin user (optional)
python manage.py createsuperuser
```

### 4. Run Application
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## Google OAuth Setup

For Google login functionality, follow the detailed guide in [`GOOGLE_OAUTH_SETUP.md`](GOOGLE_OAUTH_SETUP.md).

**Quick steps:**
1. Create Google Cloud Project
2. Enable Google+ API
3. Create OAuth 2.0 credentials
4. Update `.env` file with your credentials:
   ```env
   GOOGLE_OAUTH_CLIENT_ID=your-client-id
   GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
   ```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
```

## Usage

### For Students
1. **Sign Up** - Create account with email or Google
2. **Browse Words** - View paginated word list with search
3. **Study Flashcards** - Interactive cards with flip animations
4. **Track Progress** - Monitor learning in dashboard

### For Admins
1. **Admin Dashboard** - Manage vocabulary database
2. **Add Words** - Create new vocabulary entries
3. **Django Admin** - Full database management

## Project Structure

```
vocabulary-flash-card/
├── vocab_flashcards/          # Django project settings
├── vocabulary/                # Main app
│   ├── models.py             # Database models
│   ├── views.py              # Application views
│   ├── forms.py              # Django forms
│   └── admin.py              # Admin configuration
├── templates/                # HTML templates
│   ├── vocabulary/           # App templates
│   └── account/              # Authentication templates
├── static/                   # Static files (CSS, JS)
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
└── README.md                # This file
```

## Technology Stack

- **Backend:** Django 5.2, Python 3.10+
- **Database:** SQLite (development), PostgreSQL (production)
- **Authentication:** Django Allauth, Google OAuth
- **Frontend:** HTML5, Tailwind CSS, JavaScript
- **Deployment:** Heroku, Vercel, Railway ready

## API Endpoints

- `/` - Landing page
- `/words/` - Word list (authenticated)
- `/flashcards/` - Interactive flashcards (authenticated)
- `/dashboard/` - User dashboard (authenticated)
- `/admin-dashboard/` - Admin panel (staff only)
- `/accounts/login/` - Login page
- `/accounts/signup/` - Registration page

## Deployment

See [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) for platform-specific instructions.

### Quick Deploy to Heroku
```bash
heroku create your-app-name
heroku config:set SECRET_KEY=your-secret-key
heroku config:set GOOGLE_OAUTH_CLIENT_ID=your-client-id
heroku config:set GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
git push heroku main
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 **Documentation:** Check the guides in this repository
- 🐛 **Issues:** Report bugs via GitHub Issues
- 💬 **Discussions:** Use GitHub Discussions for questions

## Acknowledgments

- Barron's SAT 3500 vocabulary list
- Django and Python community
- Tailwind CSS for styling
- Google OAuth for authentication

---

**Made with ❤️ for SAT students worldwide**
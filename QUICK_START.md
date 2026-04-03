# Hastakala by K - Django Quick Start

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Migrations
```bash
python manage.py migrate
```

### Step 3: Create Admin User (Optional)
```bash
python manage.py createsuperuser
```

### Step 4: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 5: Start Development Server
```bash
python manage.py runserver
```

### 🌐 Access the Website
- **Homepage**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/ (if superuser created)

## 📁 Project Structure

```
hastakala_project/
├── hastakala_project/      # Django project settings
│   ├── settings.py         # Configuration (DEBUG, INSTALLED_APPS, etc.)
│   ├── urls.py             # Main URL routes
│   └── wsgi.py
├── hasta_app/              # Crochet store app
│   ├── views.py            # Logic for rendering pages
│   ├── urls.py             # App-specific routes
│   ├── models.py           # Database models (currently empty)
│   ├── templates/
│   │   └── store/
│   │       └── index.html  # Main page template
│   └── admin.py            # Admin configuration
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
└── manage.py              # Django management tool
```

## 🔗 URL Routes

| URL | View | Purpose |
|-----|------|---------|
| `/` | `home()` | Homepage with gallery |
| `/gallery/` | `gallery()` | Gallery view only |
| `/contact/submit/` | `submit_contact()` | Contact form submission |
| `/admin/` | Django Admin | Manage content & users |

## 📝 How Templates Work

Templates use Django syntax:

```html
<!-- Load static files -->
{% load static %}

<!-- Reference static files -->
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<img src="{% static 'images/logo.png' %}">

<!-- Display variables from view -->
<h1>{{ motto }}</h1>

<!-- Loop through items -->
{% for product in products %}
    <div>{{ product.name }}</div>
{% endfor %}

<!-- CSRF token for forms -->
<form method="POST">
    {% csrf_token %}
    ...
</form>
```

## 🎨 Adding Dynamic Content

### Option 1: Edit Views (Current)
1. Update `hasta_app/views.py`
2. Modify the context dictionary in the `home()` function
3. Changes appear immediately

### Option 2: Use Database Models (Better for future)
1. Define models in `hasta_app/models.py`
2. Run: `python manage.py makemigrations`
3. Run: `python manage.py migrate`
4. Access in admin: http://localhost:8000/admin/
5. Query in views: `Product.objects.all()`

## 🐛 Common Commands

```bash
# Create migration for model changes
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Create admin account
python manage.py createsuperuser

# Interactive Python shell with Django
python manage.py shell

# Check for project issues
python manage.py check

# Collect static files for production
python manage.py collectstatic

# Run tests
python manage.py test

# Run development server on specific port
python manage.py runserver 8080

# Get into Django shell
python manage.py shell
```

## 🔒 Security Notes

- Never commit `SECRET_KEY` to git
- Keep `DEBUG = False` in production
- Update `ALLOWED_HOSTS` with your domain
- Use environment variables for sensitive data
- Keep Django updated: `pip install --upgrade django`

## 📚 Useful Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Templates](https://docs.djangoproject.com/en/5.0/topics/templates/)
- [Django Models](https://docs.djangoproject.com/en/5.0/topics/db/models/)
- [Django Views](https://docs.djangoproject.com/en/5.0/topics/http/views/)

## 🛠️ Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8080  # Use different port
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear
```

### Database Errors
```bash
# Delete db.sqlite3 and re-migrate (loses data!)
python manage.py migrate
```

### Import Errors
```bash
# Check if app is in INSTALLED_APPS
# Check settings.py
```

## 📞 Next Steps

1. **Add Products to Database**: See `hasta_app/models_example.py`
2. **Style Improvements**: Modify `static/css/style.css`
3. **Add Features**: Update `hasta_app/views.py`
4. **Create Admin Forms**: Update `hasta_app/admin.py`
5. **Deploy**: See SETUP_GUIDE.md for production setup

Happy coding! 🎉

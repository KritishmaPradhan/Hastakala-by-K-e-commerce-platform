# Hastakala by K - Django Setup Guide

## Project Structure

```
hastakala_project/
├── hastakala_project/          # Main project config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py             # Project settings (installed apps, static files, etc.)
│   ├── urls.py                 # Project URL routing
│   └── wsgi.py
├── hasta_app/                  # Main app for store/products
│   ├── migrations/             # Database migrations
│   ├── templates/
│   │   └── store/
│   │       └── index.html      # Main template with Django template tags
│   ├── __init__.py
│   ├── admin.py                # Django admin setup
│   ├── apps.py
│   ├── models.py               # Database models (to be extended)
│   ├── tests.py
│   ├── urls.py                 # App-specific URLs
│   └── views.py                # Views (render templates, handle logic)
├── static/                     # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/                 # All image assets
├── templates/                  # Project-level templates (optional)
├── manage.py                   # Django management script
├── db.sqlite3                  # SQLite database
├── requirements.txt            # Python dependencies
└── README.md
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Superuser (for admin panel)
```bash
python manage.py createsuperuser
```

### 4. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 5. Run Development Server
```bash
python manage.py runserver
```

Then visit: `http://localhost:8000/`

## Key Features

### ✅ What's Been Converted to Django

- **Templates**: HTML converted to Django template with `{% load static %}` and template variables
- **Static Files**: CSS, JS, and images organized in `static/` folder
- **Views**: Main `home()` view renders the index template with context data
- **URLs**: App-based routing structure in `hasta_app/urls.py`
- **Settings**: Configured for static files, media files, and the app
- **Forms**: Django template uses `{% csrf_token %}` for security

### 📝 Template Variables Available

In `hasta_app/templates/store/index.html`:
- `{{ motto }}` - "Loops of love in every stitch"
- `{{ about_intro }}` - Business intro text
- `{{ about_description }}` - About section details
- `{{ products }}` - Gallery items from views.py
- `{{ owner_email }}` - Contact email

### 🔧 Views

#### `home()` - Main page
- Renders the homepage with all sections
- Passes product gallery data to template
- URL: `/`

#### `gallery()` - Products list
- Displays just the gallery items
- URL: `/gallery/`

#### `submit_contact()` - Contact form handler
- Currently returns JSON response (template-based form in progress)
- URL: `/contact/submit/`

## Next Steps for Enhancement

### 1. Create Models for Dynamic Data
```python
# hasta_app/models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.name}"
```

### 2. Run Migrations After Adding Models
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Update Views to Use Database
```python
from .models import Product

def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/index.html', context)
```

### 4. Handle Contact Form Properly
Update the template form to POST correctly and handle in views:
```python
def submit_contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            message=request.POST.get('message')
        )
        return redirect('store:home')
```

### 5. Register Models in Admin
```python
# hasta_app/admin.py
from django.contrib import admin
from .models import Product, ContactMessage

admin.site.register(Product)
admin.site.register(ContactMessage)
```

## Static Files Configuration

- **STATIC_URL**: `/static/` - URL prefix for static files
- **STATIC_ROOT**: `staticfiles/` - Collection directory for production
- **STATICFILES_DIRS**: `static/` - Where Django finds static files
- **MEDIA_URL**: `/media/` - URL prefix for user uploads
- **MEDIA_ROOT**: `media/` - Where user uploads are stored

Use `{% static 'path/to/file' %}` in templates to reference static files.

## Important Django Template Tags

- `{% load static %}` - Load static file tag at top of template
- `{% static 'path' %}` - Reference static files
- `{{ variable }}` - Display context variable
- `{% csrf_token %}` - CSRF protection for forms
- `{% for item in items %}...{% endfor %}` - Loop through items
- `{% if condition %}...{% endif %}` - Conditional rendering

## Running on Production

1. Set `DEBUG = False` in settings.py
2. Update `ALLOWED_HOSTS` with your domain
3. Use a production server (Gunicorn, uWSGI)
4. Use the SECRET_KEY from environment variable
5. Collect static files: `python manage.py collectstatic`
6. Use a proper database (PostgreSQL recommended)

## Useful Django Commands

```bash
# Run development server
python manage.py runserver

# Create migrations for model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin superuser
python manage.py createsuperuser

# Collect static files for production
python manage.py collectstatic

# Open Django shell for testing
python manage.py shell

# Show all installed apps
python manage.py showmigrations
```

## Documentation Links

- [Django Official Docs](https://docs.djangoproject.com/)
- [Django Templates](https://docs.djangoproject.com/en/5.0/topics/templates/)
- [Django Models](https://docs.djangoproject.com/en/5.0/topics/db/models/)
- [Django Forms](https://docs.djangoproject.com/en/5.0/topics/forms/)
- [Django Class-Based Views](https://docs.djangoproject.com/en/5.0/topics/class-based-views/)

# Django Architecture Overview

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser/Client                            │
│                   (HTML, CSS, JS)                            │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP Request
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   Django Project                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │      hastakala_project/urls.py                       │  │
│  │  (Main URL router - direct to hasta_app URLs)        │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │      hasta_app/urls.py                               │  │
│  │  (App routing - home, gallery, contact)              │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │   hasta_app/views.py                                 │  │
│  │  (Business logic - home(), gallery(), etc.)          │  │
│  │  - Prepares context data                             │  │
│  │  - Queries database (if using models)                │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │   hasta_app/templates/store/index.html               │  │
│  │  (Template rendering)                                │  │
│  │  - Django template tags: {% %}, {{ }}                │  │
│  │  - Static file references: {% static %} %}           │  │
│  │  - Loop gallery items, display variables             │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │     static/ directory                                │  │
│  │  - css/style.css (styling)                           │  │
│  │  - js/script.js (interactivity)                      │  │
│  │  - images/ (product images)                          │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
└───────────────────┼──────────────────────────────────────────┘
                    │ HTTP Response (HTML + static assets)
                    ▼
┌─────────────────────────────────────────────────────────────┐
│            Browser Renders HTML Page                         │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Request Flow

```
User Request
     │
     ▼
URL Routing (hastakala_project/urls.py)
     │
     ├─→ All requests routed to hasta_app.urls
     │
     ▼
App URL Routing (hasta_app/urls.py)
     │
     ├─→ "/" → home view
     ├─→ "/gallery/" → gallery view
     └─→ "/contact/submit/" → submit_contact view
     │
     ▼
View Function (hasta_app/views.py)
     │
     ├─→ Prepare context data
     ├─→ Query database (models)
     ├─→ Process form data if needed
     │
     ▼
Render Template with Context
     │
     ├─→ Load template file
     ├─→ Process Django tags
     ├─→ Substitute variables
     ├─→ Include static files
     │
     ▼
HTML Response + Static Assets
     │
     ▼
Browser Displays Page
```

## 📁 Directory Structure

```
hastakala_project/
│
├── hastakala_project/         # Project Configuration
│   ├── __init__.py
│   ├── settings.py            # Django settings (INSTALLED_APPS, DATABASE, etc.)
│   ├── urls.py                # Main URL router (includes hasta_app.urls)
│   ├── wsgi.py                # For production servers
│   └── asgi.py                # For async support
│
├── hasta_app/                 # Main Application
│   ├── migrations/            # Database migration history
│   ├── templates/
│   │   └── store/
│   │       └── index.html     # Main template (Django)
│   │
│   ├── __init__.py
│   ├── admin.py               # Admin configuration (with examples)
│   ├── admin_examples.py      # Example admin patterns
│   ├── apps.py                # App configuration
│   ├── models.py              # Database models (currently empty)
│   ├── models_example.py      # Example model patterns
│   ├── tests.py               # Unit tests
│   ├── urls.py                # App-specific URL routes
│   ├── views.py               # Views/Controller logic
│   ├── forms.py               # Forms (when created)
│   └── forms_example.py       # Example form patterns
│
├── static/                    # Static Files (CSS, JS, Images)
│   ├── css/
│   │   └── style.css          # Styling
│   ├── js/
│   │   └── script.js          # JavaScript for interactivity
│   └── images/                # Product images
│
├── staticfiles/               # Collected static files (production)
├── media/                     # User uploads (when configured)
│
├── templates/                 # Project-level templates (optional)
│
├── manage.py                  # Django management CLI
├── db.sqlite3                 # SQLite Database
│
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables example
│
├── QUICK_START.md            # 5-minute setup guide
├── SETUP_GUIDE.md            # Detailed setup & next steps
├── CONVERSION_SUMMARY.md     # What was changed/done
│
└── README.md                 # Original readme
```

## 🔄 Data Flow for Different Scenarios

### Scenario 1: User Loads Homepage
```
Browser → GET http://localhost:8000/
    ↓
Django URL router matches "/" to home view
    ↓
home() function in views.py executes:
    - Creates context dict with gallery data
    - Renders index.html template with context
    ↓
Template processes (index.html):
    - Loads static files (CSS, JS)
    - Loops through {{ products }}
    - Displays {{ motto }}, {{ about_intro }}, etc.
    ↓
Browser receives HTML + CSS + JS
    ↓
User sees complete website
```

### Scenario 2: User Views Gallery
```
Browser → GET http://localhost:8000/gallery/
    ↓
Django URL router matches "/gallery/" to gallery view
    ↓
gallery() function executes:
    - Gets products from context
    - Renders gallery template
    ↓
User sees gallery page
```

### Scenario 3: User Submits Contact Form
```
Browser → POST http://localhost:8000/contact/submit/
    ↓
Form data (name, email, message) sent
    ↓
Django URL router matches to submit_contact view
    ↓
submit_contact() function processes:
    - Validates CSRF token
    - Extracts POST data
    - Can save to database (when model ready)
    - Returns response
    ↓
Browser receives JSON response
    ↓
JavaScript handles response (success/error)
```

## 🗄️ Database Model (When Using Models)

```
Database (SQLite)
    │
    ├── Product table
    │   ├── id (Primary Key)
    │   ├── name
    │   ├── description
    │   ├── category
    │   ├── image
    │   └── created_at
    │
    └── ContactMessage table
        ├── id
        ├── name
        ├── email
        ├── message
        └── created_at
```

## 🔑 Key Components

### 1. URLs (Routing)
- **Type**: Configuration
- **Purpose**: Map URLs to views
- **Files**: `hastakala_project/urls.py`, `hasta_app/urls.py`

### 2. Views (Controllers)
- **Type**: Python functions/classes
- **Purpose**: Handle logic, prepare data
- **Files**: `hasta_app/views.py`
- **Returns**: Rendered HTML

### 3. Templates (Presentation)
- **Type**: HTML with Django tags
- **Purpose**: Display data to user
- **Files**: `hasta_app/templates/store/index.html`
- **Variables**: `{{ var }}`, `{% tag %}`

### 4. Models (Data)
- **Type**: Python classes mapped to database
- **Purpose**: Define database schema
- **Files**: `hasta_app/models.py` (currently empty)
- **Pending**: Create Product, ContactMessage models

### 5. Static Files
- **Type**: CSS, JS, Images
- **Purpose**: Styling and interactivity
- **Files**: `static/css/`, `static/js/`, `static/images/`

### 6. Forms (Validation)
- **Type**: Python classes
- **Purpose**: Validate user input
- **Files**: `hasta_app/forms.py` (example provided)

## 🎯 How Django Handles Different Requests

```
GET /:
    1. URL router matches "/" to home view
    2. home() creates context with products
    3. Renders index.html with context
    4. Returns HTML to browser

GET /gallery/:
    1. URL router matches "/gallery/" to gallery view
    2. gallery() prepares product data
    3. Renders gallery.html
    4. Returns HTML

POST /contact/submit/:
    1. URL router matches to submit_contact view
    2. Extracts POST data from request
    3. Validates data (CSRF token checked automatically)
    4. Can save to database
    5. Returns JSON response

GET /admin/:
    1. Django admin redirects to login if needed
    2. Admin panel loads
    3. Shows registered models
```

## 🔐 Security Features Built-In

- **CSRF Protection**: {% csrf_token %} in forms
- **SQL Injection Prevention**: ORM prevents raw SQL
- **XSS Prevention**: Template auto-escaping
- **Authentication**: User login/permissions
- **Password Hashing**: Secure password storage
- **Session Management**: Built-in sessions

## 📈 Scaling Points

1. **Database**: PostgreSQL for production
2. **Caching**: Redis for performance
3. **Static Files**: CDN for global delivery
4. **Media Files**: AWS S3 for user uploads
5. **Load Balancing**: Multiple Django instances
6. **Background Tasks**: Celery for async operations

## 🚀 Deployment Architecture

```
Production Environment:
    │
    ├── Reverse Proxy (Nginx)
    │   ├── Static file serving
    │   ├── Load balancing
    │   └── SSL/HTTPS
    │
    ├── Django Server (Gunicorn)
    │   ├── Handle requests
    │   ├── Run views
    │   └── Connect to database
    │
    ├── Database (PostgreSQL)
    │   ├── Store products
    │   ├── Store messages
    │   └── User data
    │
    └── File Storage
        ├── Static files
        ├── Media files
        └── Uploads
```

---

This architecture separates concerns (MVC pattern) and makes the codebase:
- ✅ Organized
- ✅ Maintainable
- ✅ Scalable
- ✅ Testable

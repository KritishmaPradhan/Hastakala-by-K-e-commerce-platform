// Gallery Carousel - Now uses data from database
// Fallback to hardcoded items if database data is not available
const galleryItems = typeof window.carouselItemsFromDB !== 'undefined' && window.carouselItemsFromDB.length > 0 
    ? window.carouselItemsFromDB 
    : [
        { image: '/static/images/gallery4.jpeg', title: 'Fruit Collection' },
        { image: '/static/images/gallery5.jpeg', title: 'Puffed flower' },
        { image: '/static/images/gallery6.jpeg', title: 'Flower Vine' },
        { image: '/static/images/gallery7.jpeg', title: 'Red flower Brooch' },
        { image: '/static/images/gallery8.jpeg', title: 'White daisy keyring' },
        { image: '/static/images/gallery9.jpeg', title: 'Blue Flower Keyring' },
        { image: '/static/images/gallery10.jpeg', title: 'Lavender Keyring' },
        { image: '/static/images/gallery11.jpeg', title: 'Rose Coaster' },
        { image: '/static/images/gallery12.jpeg', title: 'Kaleshi aurat clip' },
    ];

// Initialize gallery carousel
function initGalleryCarousel() {
    const galleryTrack = document.getElementById('galleryTrack');
    if (!galleryTrack) return;

    // Create gallery items HTML
    const createGalleryItemHTML = (item) => `
        <div class="gallery-item">
            <img src="${item.image}" alt="${item.title}">
            <div class="overlay">
                <h3>${item.title}</h3>
            </div>
        </div>
    `;

    // Create items multiple times to ensure continuous scrolling
    let galleryHTML = '';
    // Calculate how many repeats needed based on screen width
    // Each item is 330px wide (300px + 30px margin)
    const itemWidth = 330;
    const screenWidth = window.innerWidth;
    const itemsNeeded = Math.ceil(screenWidth / itemWidth) + 4; // Extra items for smooth transition
    
    for (let i = 0; i < itemsNeeded; i++) {
        galleryItems.forEach(item => {
            galleryHTML += createGalleryItemHTML(item);
        });
    }

    galleryTrack.innerHTML = galleryHTML;

    // After images load, measure width of one set and set animation duration
    const imgs = Array.from(galleryTrack.querySelectorAll('img'));
    const waitForImages = imgs.map(img => {
        if (img.complete) return Promise.resolve();
        return new Promise(res => img.addEventListener('load', res));
    });

    Promise.all(waitForImages).then(() => {
        // width of one set = half of track's scrollWidth (we duplicated items twice)
        const totalTrackWidth = galleryTrack.scrollWidth;
        const oneSetWidth = totalTrackWidth / 2;

        // Set speed in pixels per second (adjustable)
        const pxPerSecond = 100; // 100px/s gives a gentle scroll
        const durationSec = Math.max(10, Math.round(oneSetWidth / pxPerSecond));

        galleryTrack.style.setProperty('--carousel-duration', durationSec + 's');
    });
}

// Initialize gallery on page load
document.addEventListener('DOMContentLoaded', function() {
    initGalleryCarousel();
    initHeroSparkles();
    if (typeof initExploreWorkToggle === 'function') {
        initExploreWorkToggle();
    }
    
    // Set initial styles for animation (but NOT for gallery items - they have their own animation)
    const elements = document.querySelectorAll('.about-content, .contact-container > *');
    elements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
    });
    
    // Trigger animation on load for elements in viewport
    setTimeout(animateOnScroll, 100);
});

// Mobile Menu Toggle
const navLinks = document.getElementById('navLinks');

function showMenu() {
    navLinks.style.right = '0';
}

function hideMenu() {
    navLinks.style.right = '-200px';
}

// Profile Dropdown Toggle
function toggleProfileDropdown() {
    const dropdown = document.getElementById('profileDropdown');
    if (dropdown) {
        dropdown.classList.toggle('active');
    }
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const profileMenu = document.querySelector('.user-profile-menu');
    const dropdown = document.getElementById('profileDropdown');
    
    if (profileMenu && dropdown && !profileMenu.contains(event.target)) {
        dropdown.classList.remove('active');
    }
});

// Smooth Scrolling for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80, // Adjust for fixed header
                behavior: 'smooth'
            });
            // Close mobile menu if open
            if (window.innerWidth <= 768) {
                hideMenu();
            }
        }
    });
});


// Sticky Navigation on Scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.background = 'white';
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    }
});

// Image Lazy Loading
document.addEventListener('DOMContentLoaded', function() {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
});

// Add animation on scroll
const animateOnScroll = function() {
    const elements = document.querySelectorAll('.about-content, .contact-container > *');
    
    elements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.3;
        
        if (elementPosition < screenPosition) {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }
    });
};

window.addEventListener('scroll', animateOnScroll);

// Hero sparkle effect on hover
function initHeroSparkles() {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (window.matchMedia('(hover: none)').matches) return;

    const layer = document.createElement('div');
    layer.className = 'hero-sparkle-layer';
    hero.appendChild(layer);

    let lastSpawn = 0;
    const spawnInterval = 35;

    const spawnSparkle = (event) => {
        const now = performance.now();
        if (now - lastSpawn < spawnInterval) return;
        lastSpawn = now;

        const rect = hero.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        const sparkle = document.createElement('span');
        sparkle.className = 'hero-sparkle';
        sparkle.style.left = `${x}px`;
        sparkle.style.top = `${y}px`;
        sparkle.style.setProperty('--sparkle-drift-x', `${(Math.random() * 20 - 10).toFixed(1)}px`);
        sparkle.style.setProperty('--sparkle-drift-y', `${(-18 - Math.random() * 18).toFixed(1)}px`);
        sparkle.style.animationDuration = `${520 + Math.floor(Math.random() * 340)}ms`;

        layer.appendChild(sparkle);

        if (layer.childElementCount > 80) {
            layer.removeChild(layer.firstElementChild);
        }

        sparkle.addEventListener('animationend', () => sparkle.remove(), { once: true });
    };

    hero.addEventListener('mousemove', spawnSparkle);
}

// Animate all explore items on scroll
function animateExploreItems() {
    const items = document.querySelectorAll('.explore-item');
    items.forEach((item, index) => {
        setTimeout(() => item.classList.add('show'), index * 70);
    });
}

// Gallery Carousel
const galleryItems = [
    { image: 'images/gallery4.jpeg', title: 'crochet fruits keychain' },
    { image: 'images/gallery5.jpeg', title: 'puffed flowers' },
    { image: 'images/gallery6.jpeg', title: 'flower vine' },
    { image: 'images/gallery7.jpeg', title: 'red flower brooch' },
    { image: 'images/gallery8.jpeg', title: 'flower keychain' },
    { image: 'images/gallery4.jpeg', title: 'crochet fruits keychain' },
    { image: 'images/gallery9.jpeg', title: 'flower keychain' },
    { image: 'images/gallery10.jpeg', title: 'lavender keychain' },
    { image: 'images/gallery11.jpeg', title: 'rose coaster' },
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
    
    // Set initial styles for animation
    const elements = document.querySelectorAll('.about-content, .gallery-item, .contact-container > *');
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
    const elements = document.querySelectorAll('.about-content, .gallery-item, .contact-container > *');
    
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

// Explore Work toggle section
function initExploreWorkToggle() {
    const toggleButton = document.getElementById('exploreWorkToggle');
    const panel = document.getElementById('exploreWorkPanel');
    const grid = document.getElementById('exploreWorkGrid');

    if (!toggleButton || !panel || !grid) return;

    const exploreItems = [
        { type: 'image', src: 'images/gallery12.jpeg', alt: 'kalesi aurat clip' },
        { type: 'image', src: 'images/gallery13.jpeg', alt: 'cute chicken' },
        { type: 'image', src: 'images/gallery14.jpeg', alt: 'puffed sunflower' },
        { type: 'image', src: 'images/gallery15.jpeg', alt: 'white pink daisy' },
        { type: 'image', src: 'images/gallery16.jpeg', alt: 'purple puffed' },
        { type: 'image', src: 'images/gallery17.jpeg', alt: 'pink puffed' },
        { type: 'image', src: 'images/gallery18.jpeg', alt: 'blue puffed' },
        { type: 'image', src: 'images/gallery19.jpeg', alt: 'twin octo' },
        { type: 'image', src: 'images/gallery20.jpeg', alt: 'happy sad octo' },
        { type: 'image', src: 'images/gallery21.jpeg', alt: 'white daisy' },
        { type: 'image', src: 'images/gallery22.jpeg', alt: 'sunflower' },
        { type: 'image', src: 'images/gallery23.jpeg', alt: 'bow pair' },
        { type: 'image', src: 'images/gallery24.jpeg', alt: 'flower vine white' },
        { type: 'image', src: 'images/gallery25.jpeg', alt: 'rose' },
    ];

    const renderItems = () => {
        grid.innerHTML = exploreItems.map((item) => {
            if (item.type === 'image') {
                return `
                    <article class="explore-item">
                        <img src="${item.src}" alt="${item.alt}">
                    </article>
                `;
            }

            return `
                <article class="explore-item">
                    <div class="explore-placeholder">${item.label}</div>
                </article>
            `;
        }).join('');
    };

    const animateIn = () => {
        const cards = Array.from(grid.querySelectorAll('.explore-item'));
        cards.forEach((card, index) => {
            setTimeout(() => card.classList.add('show'), index * 70);
        });
    };

    toggleButton.addEventListener('click', () => {
        const isOpen = panel.classList.contains('is-open');

        if (isOpen) {
            panel.classList.remove('is-open');
            panel.setAttribute('aria-hidden', 'true');
            toggleButton.setAttribute('aria-expanded', 'false');

            setTimeout(() => {
                if (!panel.classList.contains('is-open')) {
                    grid.innerHTML = '';
                }
            }, 380);
            return;
        }

        renderItems();
        panel.classList.add('is-open');
        panel.setAttribute('aria-hidden', 'false');
        toggleButton.setAttribute('aria-expanded', 'true');

        requestAnimationFrame(animateIn);
    });
}

// swipe gallery carousel
const next = document.querySelector('.next');
const prev = document.querySelector('.prev');
const slide = document.querySelector('.slide');

if (next && prev && slide) {
    next.addEventListener('click', function(){
        const items = slide.querySelectorAll('.item');
        if (items.length) slide.appendChild(items[0]);
    });

    prev.addEventListener('click', function(){
        const items = slide.querySelectorAll('.item');
        if (items.length) slide.prepend(items[items.length - 1]); // here the length of items = 6
    });
}

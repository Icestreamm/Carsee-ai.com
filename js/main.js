// Mobile Menu Toggle
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const navMenu = document.getElementById('navMenu');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        mobileMenuToggle.classList.toggle('active');
    });
}

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    if (navMenu && !navMenu.contains(e.target) && !mobileMenuToggle.contains(e.target)) {
        navMenu.classList.remove('active');
        mobileMenuToggle.classList.remove('active');
    }
});

// Survey Banner Close
const closeBanner = document.getElementById('closeBanner');
const surveyBanner = document.getElementById('surveyBanner');

if (closeBanner) {
    closeBanner.addEventListener('click', () => {
        surveyBanner.style.display = 'none';
        localStorage.setItem('surveyBannerClosed', 'true');
    });
}

// Check if banner was previously closed
if (localStorage.getItem('surveyBannerClosed') === 'true') {
    if (surveyBanner) {
        surveyBanner.style.display = 'none';
    }
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Dropdown menu handling
document.querySelectorAll('.nav-item.dropdown').forEach(item => {
    const link = item.querySelector('.nav-link');
    const menu = item.querySelector('.dropdown-menu');
    
    if (window.innerWidth <= 992) {
        // Mobile: toggle on click
        link.addEventListener('click', (e) => {
            e.preventDefault();
            menu.classList.toggle('active');
        });
    }
});

// Language selector
const languageSelector = document.querySelector('.language-selector');
if (languageSelector) {
    languageSelector.addEventListener('click', (e) => {
        e.stopPropagation();
    });
}

// Close dropdowns when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-item.dropdown')) {
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.classList.remove('active');
        });
    }
});

// Contact and Demo button handlers (now links, so no special handling needed)
// Links will navigate naturally

// Partner logos animation
const partnerLogos = document.querySelectorAll('.partners-logos img, .partners-mentors-logos img');
partnerLogos.forEach((logo, index) => {
    logo.style.transition = `opacity 0.3s ease ${index * 0.1}s`;
});

// Header scroll opacity (carsee_b2b)
const header = document.querySelector('.header');
if (header) {
    window.addEventListener('scroll', () => {
        header.classList.toggle('scrolled', window.scrollY > 40);
    }, { passive: true });
}

// Form validation (if forms are added later)
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.style.borderColor = '#ff0000';
        } else {
            input.style.borderColor = '';
        }
    });
    
    return isValid;
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    console.log('CarSee website loaded');
    
    // Add any initialization code here
});

/* ── PAGE LOAD SEQUENCE ── */
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => document.body.classList.add('page-loaded'), 60);
});

/* ── SCROLL ANIMATION OBSERVER ── */
(function() {
    const cardSelectors = [
        '.feature-card',
        '.solution-card',
        '.professional-card',
        '.step-item',
        '.partner-logo',
        '.stat-item'
    ];
    const titleSelectors = [
        '.section-title',
        '.section-subtitle'
    ];
    const processStepSelector = '.process-step';
    const partnerLogoSelector = '.partners-logos img, .partners-mentors-logos img';

    cardSelectors.forEach(sel => {
        document.querySelectorAll(sel).forEach(el => {
            el.classList.add('carsee-animate');
        });
    });
    document.querySelectorAll(processStepSelector).forEach(el => {
        el.classList.add('carsee-animate');
    });
    document.querySelectorAll(partnerLogoSelector).forEach(el => {
        el.classList.add('carsee-animate');
    });

    titleSelectors.forEach(sel => {
        document.querySelectorAll(sel).forEach(el => {
            el.classList.add('carsee-animate-title');
        });
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.12,
        rootMargin: '0px 0px -40px 0px'
    });

    document.querySelectorAll('.carsee-animate, .carsee-animate-title').forEach(el => observer.observe(el));
})();

/* ── STAT NUMBER COUNTER ── */
(function() {
    function easeOutExpo(t) {
        return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
    }

    function animateCounter(el) {
        const raw    = el.dataset.target;
        const suffix = el.dataset.suffix || '';
        const target = parseFloat(raw);
        const isFloat = raw.includes('.');
        const decimals = isFloat ? raw.split('.')[1].length : 0;
        const duration = 1800;
        const start    = performance.now();

        function tick(now) {
            const elapsed  = now - start;
            const progress = Math.min(elapsed / duration, 1);
            const eased    = easeOutExpo(progress);
            const current  = target * eased;
            el.textContent = isFloat
                ? current.toFixed(decimals) + suffix
                : Math.floor(current) + suffix;
            if (progress < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
    }

    const statObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                statObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.stat-number, .stat-value').forEach(el => {
        const text   = el.textContent.trim();
        const num    = parseFloat(text.replace(/[^0-9.]/g, ''));
        const suffix = text.replace(/[0-9.]/g, '');
        if (!isNaN(num)) {
            el.dataset.target  = num;
            el.dataset.suffix  = suffix;
            el.textContent     = '0' + suffix;
            statObserver.observe(el);
        }
    });
})();

/* ── FLOATING CTA VISIBILITY ── */
(function() {
    const btn    = document.getElementById('floatingCta');
    if (!btn) return;

    const footer = document.querySelector('footer, .footer');
    const SHOW_AFTER = 600;

    function update() {
        const scrollY      = window.scrollY;
        const windowHeight = window.innerHeight;
        const docHeight    = document.documentElement.scrollHeight;

        const nearFooter = footer
            ? window.scrollY + windowHeight >= footer.offsetTop - 100
            : scrollY > docHeight - windowHeight - 300;

        if (scrollY > SHOW_AFTER && !nearFooter) {
            btn.classList.add('is-visible');
        } else {
            btn.classList.remove('is-visible');
        }
    }

    window.addEventListener('scroll', update, { passive: true });
    update();
})();

/**
 * Cookie Consent Management
 * Handles cookie consent banner and user preferences
 */

(function () {
    'use strict';

    // Configuration
    const CONSENT_STORAGE_KEY = 'carsee_cookie_consent';
    const BANNER_ID = 'cookieBanner';
    const SETTINGS_MODAL_ID = 'cookieSettingsModal';

    /** Resolve cookies.css URL from this script’s src (works for any folder depth). */
    function getCookieCssHref() {
        var src = '';
        try {
            if (document.currentScript && document.currentScript.src) {
                src = document.currentScript.src;
            }
        } catch (e) { /* ignore */ }
        if (!src) {
            var nodes = document.querySelectorAll('script[src*="cookies.js"]');
            if (nodes.length) {
                var raw = nodes[nodes.length - 1].getAttribute('src') || '';
                try {
                    src = new URL(raw, window.location.href).href;
                } catch (e2) {
                    src = raw;
                }
            }
        }
        if (!src) return '';
        return src.replace(/\/js\/cookies\.js(\?.*)?$/i, '/css/cookies.css');
    }

    /** Ensure cookies.css is loaded before showing UI (avoids unstyled banner when HTML omits the link). */
    function ensureCookieStylesheet(done) {
        function finish() {
            if (typeof done === 'function') done();
        }
        var href = getCookieCssHref();
        if (!href) {
            finish();
            return;
        }
        var links = document.querySelectorAll('link[rel="stylesheet"][href*="cookies.css"]');
        for (var i = 0; i < links.length; i++) {
            if (links[i].href.indexOf('cookies.css') !== -1) {
                finish();
                return;
            }
        }
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = href;
        link.setAttribute('data-carsee-cookies', '1');
        var called = false;
        function once() {
            if (called) return;
            called = true;
            finish();
        }
        link.onload = once;
        link.onerror = once;
        document.head.appendChild(link);
        if (link.sheet) {
            try {
                var rules = link.sheet.cssRules;
                if (rules && rules.length) once();
            } catch (e3) { /* cross-origin or not ready */ }
        }
        window.setTimeout(once, 1800);
    }

    // Detect language from URL or HTML lang attribute (used by href helpers below)
    const isArabic = window.location.pathname.includes('/ar/') ||
                     document.documentElement.lang === 'ar';

    /** Cookies policy page: correct ../ depth from any folder (EN + /ar/). */
    function cookiesPolicyHref() {
        var parts = window.location.pathname.split('/').filter(Boolean);
        if (!parts.length) return 'cookies.html';
        var depth;
        if (parts[0] === 'ar') {
            depth = Math.max(0, parts.length - 2);
        } else {
            depth = Math.max(0, parts.length - 1);
        }
        return new Array(depth + 1).join('../') + 'cookies.html';
    }

    // Content based on language
    const content = isArabic ? {
        preferencesTitle: 'إعدادات ملفات التعريف',
        title: 'نحتاج موافقتك على ملفات تعريف الارتباط',
        description: 'نستخدم ملفات تعريف الارتباط لتحسين تجربتك على موقعنا. اختر ما إذا كنت تقبل أنواع مختلفة من ملفات تعريف الارتباط.',
        acceptAll: 'قبول الكل',
        reject: 'رفض',
        manage: 'إدارة التفضيلات',
        learnMore: 'اعرف المزيد',
        essential: 'ضروري',
        performance: 'الأداء',
        functional: 'الوظيفة',
        marketing: 'التسويق',
        essentialDesc: 'ضروري لعمل الموقع. لا يمكن تعطيله.',
        performanceDesc: 'يساعدنا على فهم كيفية استخدامك للموقع.',
        functionalDesc: 'يتذكر اختياراتك وتفضيلاتك.',
        marketingDesc: 'يستخدم لتقديم إعلانات ذات صلة.',
        save: 'حفظ التفضيلات',
        close: 'إغلاق'
    } : {
        preferencesTitle: 'Cookie Preferences',
        title: 'We Need Your Cookie Consent',
        description: 'We use cookies to improve your experience on our website. Choose whether you accept different types of cookies.',
        acceptAll: 'Accept All',
        reject: 'Reject',
        manage: 'Manage Preferences',
        learnMore: 'Learn More',
        essential: 'Essential',
        performance: 'Performance',
        functional: 'Functional',
        marketing: 'Marketing',
        essentialDesc: 'Required for the website to function. Cannot be disabled.',
        performanceDesc: 'Helps us understand how you use our site.',
        functionalDesc: 'Remembers your choices and preferences.',
        marketingDesc: 'Used to deliver relevant advertisements.',
        save: 'Save Preferences',
        close: 'Close'
    };

    // Cookie preference defaults
    const defaultPreferences = {
        essential: true,  // Always required
        performance: false,
        functional: false,
        marketing: false
    };

    // Get saved preferences or return defaults
    function getPreferences() {
        const saved = localStorage.getItem(CONSENT_STORAGE_KEY);
        if (saved) {
            try {
                return JSON.parse(saved);
            } catch (e) {
                return defaultPreferences;
            }
        }
        return defaultPreferences;
    }

    // Save preferences to localStorage
    function savePreferences(prefs) {
        localStorage.setItem(CONSENT_STORAGE_KEY, JSON.stringify(prefs));
    }

    // Check if user has made a consent choice
    function hasConsentChoice() {
        return localStorage.getItem(CONSENT_STORAGE_KEY) !== null;
    }

    // Create and inject the cookie banner HTML
    function createBanner() {
        const dir = isArabic ? 'rtl' : 'ltr';
        const banner = document.createElement('div');
        banner.id = BANNER_ID;
        banner.className = 'cookie-banner';
        banner.setAttribute('dir', dir);
        banner.innerHTML = `
            <div class="cookie-banner-content">
                <div class="cookie-banner-text">
                    <h3>${content.title}</h3>
                    <p>${content.description}</p>
                    <a href="${cookiesPolicyHref()}" class="cookie-learn-more">${content.learnMore}</a>
                </div>
                <div class="cookie-banner-actions">
                    <button class="cookie-btn cookie-btn-reject">${content.reject}</button>
                    <button class="cookie-btn cookie-btn-manage">${content.manage}</button>
                    <button class="cookie-btn cookie-btn-accept">${content.acceptAll}</button>
                </div>
            </div>
        `;
        document.body.appendChild(banner);
        return banner;
    }

    // Create settings modal
    function createSettingsModal() {
        const dir = isArabic ? 'rtl' : 'ltr';
        const modal = document.createElement('div');
        modal.id = SETTINGS_MODAL_ID;
        modal.className = 'cookie-settings-modal';
        modal.setAttribute('dir', dir);
        modal.innerHTML = `
            <div class="cookie-settings-overlay" aria-hidden="true"></div>
            <div class="cookie-settings-content" role="dialog" aria-modal="true" aria-labelledby="cookie-settings-title">
                <div class="cookie-settings-header">
                    <h2 id="cookie-settings-title">${content.preferencesTitle}</h2>
                    <button type="button" class="cookie-settings-close" aria-label="${content.close}">&times;</button>
                </div>
                <div class="cookie-settings-body">
                    <div class="cookie-setting-item">
                        <div class="cookie-setting-header">
                            <input type="checkbox" id="cookie-essential" checked disabled>
                            <label for="cookie-essential">${content.essential}</label>
                        </div>
                        <p>${content.essentialDesc}</p>
                    </div>
                    <div class="cookie-setting-item">
                        <div class="cookie-setting-header">
                            <input type="checkbox" id="cookie-performance">
                            <label for="cookie-performance">${content.performance}</label>
                        </div>
                        <p>${content.performanceDesc}</p>
                    </div>
                    <div class="cookie-setting-item">
                        <div class="cookie-setting-header">
                            <input type="checkbox" id="cookie-functional">
                            <label for="cookie-functional">${content.functional}</label>
                        </div>
                        <p>${content.functionalDesc}</p>
                    </div>
                    <div class="cookie-setting-item">
                        <div class="cookie-setting-header">
                            <input type="checkbox" id="cookie-marketing">
                            <label for="cookie-marketing">${content.marketing}</label>
                        </div>
                        <p>${content.marketingDesc}</p>
                    </div>
                </div>
                <div class="cookie-settings-footer">
                    <button type="button" class="cookie-btn cookie-btn-save">${content.save}</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        return modal;
    }

    // Load preferences into modal checkboxes
    function loadPreferencesToModal(prefs) {
        const modal = document.getElementById(SETTINGS_MODAL_ID);
        if (!modal) return;

        document.getElementById('cookie-essential').checked = true;
        document.getElementById('cookie-performance').checked = prefs.performance || false;
        document.getElementById('cookie-functional').checked = prefs.functional || false;
        document.getElementById('cookie-marketing').checked = prefs.marketing || false;
    }

    // Get current preferences from modal
    function getPreferencesFromModal() {
        return {
            essential: true,
            performance: document.getElementById('cookie-performance').checked,
            functional: document.getElementById('cookie-functional').checked,
            marketing: document.getElementById('cookie-marketing').checked
        };
    }

    // Show banner
    function showBanner() {
        const banner = document.getElementById(BANNER_ID);
        if (banner) {
            banner.classList.add('show');
            banner.style.display = '';
        }
    }

    // Hide banner
    function hideBanner() {
        const banner = document.getElementById(BANNER_ID);
        if (banner) {
            banner.classList.remove('show');
            banner.style.display = 'none';
        }
    }

    // Show settings modal
    function showSettingsModal() {
        const modal = document.getElementById(SETTINGS_MODAL_ID);
        if (modal) {
            modal.classList.add('show');
            modal.style.display = '';
            loadPreferencesToModal(getPreferences());
        }
    }

    // Hide settings modal
    function hideSettingsModal() {
        const modal = document.getElementById(SETTINGS_MODAL_ID);
        if (modal) {
            modal.classList.remove('show');
            modal.style.display = 'none';
        }
    }

    // Handle accept all
    function handleAcceptAll() {
        const prefs = {
            essential: true,
            performance: true,
            functional: true,
            marketing: true
        };
        savePreferences(prefs);
        hideBanner();
        loadAnalytics();
    }

    // Handle reject
    function handleReject() {
        const prefs = {
            essential: true,
            performance: false,
            functional: false,
            marketing: false
        };
        savePreferences(prefs);
        hideBanner();
    }

    // Handle save preferences
    function handleSavePreferences() {
        const prefs = getPreferencesFromModal();
        savePreferences(prefs);
        hideSettingsModal();
        hideBanner();
        if (prefs.performance || prefs.marketing) {
            loadAnalytics();
        }
    }

    // Load analytics if consent given
    function loadAnalytics() {
        const prefs = getPreferences();
        if (prefs.performance && !window.GA_LOADED) {
            // Load Google Analytics or other tracking here
            window.GA_LOADED = true;
            // Example: load gtag script
            // const script = document.createElement('script');
            // script.async = true;
            // script.src = 'https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID';
            // document.head.appendChild(script);
        }
    }

    // Initialize on DOM ready
    function init() {
        ensureCookieStylesheet(function () {
            createBanner();
            createSettingsModal();

            if (!hasConsentChoice()) {
                showBanner();
            } else {
                loadAnalytics();
            }

            bindEvents();
        });
    }

    // Bind event listeners
    function bindEvents() {
        // Banner buttons
        const acceptBtn = document.querySelector('.cookie-btn-accept');
        const rejectBtn = document.querySelector('.cookie-btn-reject');
        const manageBtn = document.querySelector('.cookie-btn-manage');

        if (acceptBtn) acceptBtn.addEventListener('click', handleAcceptAll);
        if (rejectBtn) rejectBtn.addEventListener('click', handleReject);
        if (manageBtn) manageBtn.addEventListener('click', showSettingsModal);

        // Settings modal buttons
        const saveBtn = document.querySelector('.cookie-btn-save');
        const closeBtn = document.querySelector('.cookie-settings-close');
        const overlay = document.querySelector('.cookie-settings-overlay');

        if (saveBtn) saveBtn.addEventListener('click', handleSavePreferences);
        if (closeBtn) closeBtn.addEventListener('click', hideSettingsModal);
        if (overlay) overlay.addEventListener('click', hideSettingsModal);

        // Cookies settings link in footer
        const cookieSettingsLink = document.getElementById('cookiesSettings');
        if (cookieSettingsLink) {
            cookieSettingsLink.addEventListener('click', function(e) {
                e.preventDefault();
                showSettingsModal();
            });
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose API for manual control
    window.CarSeeCookies = {
        showBanner: showBanner,
        hideBanner: hideBanner,
        showSettings: showSettingsModal,
        getPreferences: getPreferences,
        savePreferences: savePreferences
    };
})();

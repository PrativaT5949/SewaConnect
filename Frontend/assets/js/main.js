// ===============================
// Load Header & Footer
// ===============================

async function loadComponent(id, file) {
    try {
        const response = await fetch(file);

        if (!response.ok) {
            throw new Error(`Failed to load ${file}`);
        }

        const html = await response.text();
        document.getElementById(id).innerHTML = html;
    } catch (error) {
        console.error(error);
    }
}

// ===============================
// Navbar
// ===============================

function initializeNavbar() {
    const navToggle = document.getElementById("navToggle");
    const mobilePanel = document.getElementById("mobilePanel");

    if (!navToggle || !mobilePanel) return;

    navToggle.addEventListener("click", () => {
        navToggle.classList.toggle("active");
        mobilePanel.classList.toggle("open");
    });

    mobilePanel.querySelectorAll("a").forEach((a) => {
        a.addEventListener("click", () => {
            navToggle.classList.remove("active");
            mobilePanel.classList.remove("open");
        });
    });
}

// ===============================
// Counter Animation
// ===============================

function initializeCounters() {
    const counters = document.querySelectorAll(".count-up");

    if (!counters.length) return;

    const animateCounter = (el) => {
        const target = parseFloat(el.dataset.target);
        const decimals = parseInt(el.dataset.decimals || "0");
        const suffix = el.dataset.suffix || "";
        const duration = 1800;
        const start = performance.now();

        const step = (now) => {
            const progress = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const value = target * eased;

            el.textContent = value.toFixed(decimals) + suffix;

            if (progress < 1) {
                requestAnimationFrame(step);
            }
        };

        requestAnimationFrame(step);
    };

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 0.5,
        }
    );

    counters.forEach((counter) => observer.observe(counter));
}

// ===============================
// Testimonial Slider
// ===============================

function initializeTestimonials() {
    const slidesWrap = document.getElementById("testiSlides");
    const dotsWrap = document.getElementById("testiDots");
    const prevBtn = document.getElementById("testiPrev");
    const nextBtn = document.getElementById("testiNext");
    const wrapper = document.querySelector(".testi-wrap");

    if (
        !slidesWrap ||
        !dotsWrap ||
        !prevBtn ||
        !nextBtn ||
        !wrapper
    )
        return;

    const slides = slidesWrap.children;
    let current = 0;

    for (let i = 0; i < slides.length; i++) {
        const dot = document.createElement("button");

        if (i === 0) {
            dot.classList.add("active");
        }

        dot.addEventListener("click", () => goTo(i));

        dotsWrap.appendChild(dot);
    }

    function goTo(index) {
        current = (index + slides.length) % slides.length;

        slidesWrap.style.transform = `translateX(-${current * 100}%)`;

        [...dotsWrap.children].forEach((dot, i) => {
            dot.classList.toggle("active", i === current);
        });
    }

    prevBtn.addEventListener("click", () => goTo(current - 1));

    nextBtn.addEventListener("click", () => goTo(current + 1));

    let autoSlide = setInterval(() => {
        goTo(current + 1);
    }, 6000);

    wrapper.addEventListener("mouseenter", () => {
        clearInterval(autoSlide);
    });

    wrapper.addEventListener("mouseleave", () => {
        autoSlide = setInterval(() => {
            goTo(current + 1);
        }, 6000);
    });
}

// ===============================
// FAQ Accordion
// ===============================

function initializeFAQ() {
    const faqItems = document.querySelectorAll(".faq-item");

    if (!faqItems.length) return;

    faqItems.forEach((item) => {
        const question = item.querySelector(".faq-q");
        const answer = item.querySelector(".faq-a");

        if (item.classList.contains("open")) {
            answer.style.maxHeight = answer.scrollHeight + "px";
        }

        question.addEventListener("click", () => {
            const isOpen = item.classList.contains("open");

            faqItems.forEach((other) => {
                other.classList.remove("open");

                const otherAnswer = other.querySelector(".faq-a");

                if (otherAnswer) {
                    otherAnswer.style.maxHeight = null;
                }
            });

            if (!isOpen) {
                item.classList.add("open");
                answer.style.maxHeight = answer.scrollHeight + "px";
            }
        });
    });
}

// ===============================
// Initialize Everything
// ===============================

async function initPage() {
    await loadComponent("header", "components/header.html");
    await loadComponent("footer", "components/footer.html");

    initializeNavbar();
    initializeCounters();
    initializeTestimonials();
    initializeFAQ();
}

document.addEventListener("DOMContentLoaded", initPage);
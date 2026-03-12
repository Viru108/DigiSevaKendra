document.addEventListener('DOMContentLoaded', () => {
    // Intersection Observer for Reveal animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Apply reveal to elements
    const elementsToReveal = document.querySelectorAll('.reveal, section, .glass-card');
    elementsToReveal.forEach((el, index) => {
        if (!el.classList.contains('reveal')) {
            el.classList.add('reveal');
        }

        // Add stagger if in a grid
        if (el.parentElement.classList.contains('row') || el.parentElement.classList.contains('bento-grid')) {
            const staggerIdx = (index % 3) + 1;
            el.classList.add(`stagger-${staggerIdx}`);
        }

        revealObserver.observe(el);
    });

    // Dynamic background blob & Cursor Follower
    const follower = document.createElement('div');
    follower.className = 'cursor-follower';
    document.body.appendChild(follower);

    let ticket;
    document.addEventListener('mousemove', (e) => {
        if (ticket) cancelAnimationFrame(ticket);

        ticket = requestAnimationFrame(() => {
            const x = e.clientX;
            const y = e.clientY;

            // Move Follower
            if (follower) {
                follower.style.left = `${x}px`;
                follower.style.top = `${y}px`;
            }

            const xRel = (x / window.innerWidth - 0.5) * 2;
            const yRel = (y / window.innerHeight - 0.5) * 2;

            const blob1 = document.querySelector('.blob-1');
            const blob2 = document.querySelector('.blob-2');

            if (blob1) blob1.style.transform = `translate(${xRel * 60}px, ${yRel * 60}px)`;
            if (blob2) blob2.style.transform = `translate(${-(xRel * 80)}px, ${-(yRel * 80)}px)`;
        });
    });

    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

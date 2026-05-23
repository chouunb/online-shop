document.addEventListener('DOMContentLoaded', () => {

    // Плавное появление карточек
    const animatedElements =
        document.querySelectorAll(
            '.category-card, .feature-card'
        );

    const observer =
        new IntersectionObserver((entries) => {

            entries.forEach((entry) => {

                if (entry.isIntersecting) {

                    entry.target.classList.add('show');
                }
            });

        }, {
            threshold: 0.15
        });

    animatedElements.forEach((element) => {

        element.classList.add('hidden-card');

        observer.observe(element);
    });

    // Параллакс glow
    const glow1 =
        document.querySelector('.hero-glow-1');

    const glow2 =
        document.querySelector('.hero-glow-2');

    document.addEventListener('mousemove', (event) => {

        const x = event.clientX / window.innerWidth;
        const y = event.clientY / window.innerHeight;

        glow1.style.transform =
            `translate(${x * 40}px, ${y * 40}px)`;

        glow2.style.transform =
            `translate(${-x * 40}px, ${-y * 40}px)`;
    });

});
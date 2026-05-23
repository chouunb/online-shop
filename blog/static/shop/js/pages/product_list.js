import BatchLoader from '../batch-loader.js';

new BatchLoader("productsContainer");

import BatchLoader from "../batch-loader.js";

window.productsBatchLoader =
    new BatchLoader('productsContainer');

document.addEventListener('DOMContentLoaded', () => {

    initParallax();
    initRevealAnimations();

});

function initRevealAnimations() {

    const cards =
        document.querySelectorAll('.product-card');

    const observer =
        new IntersectionObserver((entries) => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.target.classList.add('show-card');

                }

            });

        }, {
            threshold: 0.15
        });

    cards.forEach(card => {
        observer.observe(card);
    });

}

function initParallax() {

    const hero =
        document.querySelector('.products-hero');

    if (!hero) return;

    window.addEventListener('mousemove', (e) => {

        const x =
            (window.innerWidth / 2 - e.clientX) / 40;

        const y =
            (window.innerHeight / 2 - e.clientY) / 40;

        hero.style.transform =
            `translate(${x}px, ${y}px)`;

    });

}
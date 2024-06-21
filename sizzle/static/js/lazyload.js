document.addEventListener("DOMContentLoaded", function () {
    const lazySections = document.querySelectorAll('.kursus-section, .resep-section');

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        rootMargin: '0px',
        threshold: 0.1
    });

    lazySections.forEach(section => {
        observer.observe(section);
    });
});

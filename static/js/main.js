document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) {
    lucide.createIcons();
  }

  // AOS
  if (window.AOS) {
    AOS.init({
      duration: 750,
      easing: 'ease-out-cubic',
      once: true,
      offset: 80,
    });
  }

  // Sticky header
  const header = document.getElementById('site-header');
  if (header) {
    const onScroll = () => {
      header.classList.toggle('scrolled', window.scrollY > 40);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // GSAP hero entrance + parallax
  if (window.gsap) {
    gsap.registerPlugin(ScrollTrigger);

    const heroItems = gsap.utils.toArray('[data-hero]');
    if (heroItems.length) {
      gsap.to(heroItems, {
        opacity: 1,
        y: 0,
        duration: 0.9,
        stagger: 0.12,
        ease: 'power3.out',
        delay: 0.15,
      });
    }

    if (document.querySelector('.hero-bg')) {
      gsap.to('.hero-bg', {
        yPercent: 12,
        ease: 'none',
        scrollTrigger: {
          trigger: '#hero',
          start: 'top top',
          end: 'bottom top',
          scrub: true,
        },
      });
    }
  } else {
    document.querySelectorAll('.hero-fade').forEach((el) => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
  }

  // Counters
  const counters = document.querySelectorAll('.counter');
  const animateCounter = (el) => {
    const target = Number(el.dataset.target) || 0;
    const duration = 1400;
    const start = performance.now();

    const tick = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(target * eased).toLocaleString('ru-RU');
      if (progress < 1) requestAnimationFrame(tick);
      else el.textContent = target.toLocaleString('ru-RU');
    };

    requestAnimationFrame(tick);
  };

  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !entry.target.dataset.done) {
            entry.target.dataset.done = '1';
            animateCounter(entry.target);
          }
        });
      },
      { threshold: 0.4 }
    );
    counters.forEach((c) => io.observe(c));
  } else {
    counters.forEach(animateCounter);
  }

  // Toasts
  document.querySelectorAll('.toast-close').forEach((btn) => {
    btn.addEventListener('click', () => {
      btn.closest('.toast')?.remove();
    });
  });

  // Scroll to contacts if hash present after form post or form errors
  if (window.location.hash === '#contacts' || document.querySelector('.consult-form .has-error')) {
    const contacts = document.getElementById('contacts');
    if (contacts) {
      setTimeout(() => contacts.scrollIntoView({ behavior: 'smooth' }), 100);
    }
  }

  // Info modal for clickable cards
  const modal = document.getElementById('info-modal');
  const modalBody = document.getElementById('info-modal-body');
  let lastTrigger = null;

  const openModal = (targetId, trigger) => {
    const source = document.getElementById(targetId);
    if (!modal || !modalBody || !source) return;

    lastTrigger = trigger || null;
    modalBody.innerHTML = source.innerHTML;
    modal.hidden = false;
    modal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');

    if (window.lucide) lucide.createIcons();

    modal.querySelector('.info-modal__close')?.focus();
  };

  const closeModal = (scrollToHash) => {
    if (!modal || !modalBody) return;
    modal.hidden = true;
    modal.setAttribute('aria-hidden', 'true');
    modalBody.innerHTML = '';
    document.body.classList.remove('modal-open');
    lastTrigger?.focus();
    lastTrigger = null;

    if (scrollToHash && scrollToHash.startsWith('#')) {
      const target = document.querySelector(scrollToHash);
      if (target) setTimeout(() => target.scrollIntoView({ behavior: 'smooth' }), 80);
    }
  };

  document.querySelectorAll('[data-detail-target]').forEach((btn) => {
    btn.addEventListener('click', () => {
      openModal(btn.getAttribute('data-detail-target'), btn);
    });
  });

  modal?.addEventListener('click', (e) => {
    const closer = e.target.closest('[data-modal-close]');
    if (!closer) return;
    const href = closer.getAttribute('href');
    if (closer.tagName === 'A') e.preventDefault();
    closeModal(href);
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && !modal.hidden) closeModal();
  });
});

document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) {
    lucide.createIcons();
  }

  if (window.AOS) {
    AOS.init({
      duration: 800,
      easing: 'ease-out-cubic',
      once: true,
      offset: 70,
      delay: 0,
    });
  }

  const header = document.getElementById('site-header');
  if (header) {
    const onScroll = () => {
      header.classList.toggle('scrolled', window.scrollY > 40);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  if (window.gsap) {
    gsap.registerPlugin(ScrollTrigger);

    const heroItems = gsap.utils.toArray('[data-hero]');
    if (heroItems.length) {
      gsap.to(heroItems, {
        opacity: 1,
        y: 0,
        duration: 1,
        stagger: 0.11,
        ease: 'power3.out',
        delay: 0.12,
      });
    }

    if (document.querySelector('.hero-bg-img')) {
      gsap.to('.hero-bg-img', {
        yPercent: 10,
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

  // CountUp
  const counters = document.querySelectorAll('.counter');
  const animateCounter = (el) => {
    const target = Number(el.dataset.target) || 0;
    const duration = 1600;
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
      { threshold: 0.35 }
    );
    counters.forEach((c) => io.observe(c));
  } else {
    counters.forEach(animateCounter);
  }

  // Button ripple
  document.querySelectorAll('.btn-ripple').forEach((btn) => {
    btn.addEventListener('click', function (e) {
      const rect = this.getBoundingClientRect();
      const circle = document.createElement('span');
      const size = Math.max(rect.width, rect.height);
      circle.className = 'ripple';
      circle.style.width = circle.style.height = `${size}px`;
      circle.style.left = `${e.clientX - rect.left - size / 2}px`;
      circle.style.top = `${e.clientY - rect.top - size / 2}px`;
      this.appendChild(circle);
      setTimeout(() => circle.remove(), 650);
    });
  });

  document.querySelectorAll('.toast-close').forEach((btn) => {
    btn.addEventListener('click', () => {
      btn.closest('.toast')?.remove();
    });
  });

  if (window.location.hash === '#contacts' || document.querySelector('.consult-form .has-error')) {
    const contacts = document.getElementById('contacts');
    if (contacts) {
      setTimeout(() => contacts.scrollIntoView({ behavior: 'smooth' }), 100);
    }
  }

  // Modal
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

  // Form loading state
  const form = document.querySelector('.consult-form');
  if (form) {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('button[type="submit"]');
      if (btn && form.checkValidity()) {
        btn.disabled = true;
        btn.style.opacity = '0.75';
        btn.innerHTML = 'Отправка…';
      }
    });
  }
});

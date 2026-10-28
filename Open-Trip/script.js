
    // Configure with the verified admin WhatsApp number, country code included and no + or spaces, to enable direct sending.
    const WHATSAPP_NUMBER = "";
    const $ = (selector, scope = document) => scope.querySelector(selector);
    const $$ = (selector, scope = document) => [...scope.querySelectorAll(selector)];

    // Header shadow and reading progress.
    const header = $('.site-header');
    const progress = $('.page-progress');
    const updateScrollUI = () => {
      const scrollable = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = `${scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0}%`;
      header.classList.toggle('scrolled', window.scrollY > 12);
    };
    window.addEventListener('scroll', updateScrollUI, { passive: true });
    updateScrollUI();

    // Reveal sections gently as they enter the viewport.
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if ('IntersectionObserver' in window && !reduceMotion) {
      const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -36px 0px' });
      $$('.reveal').forEach((element) => revealObserver.observe(element));
    } else {
      $$('.reveal').forEach((element) => element.classList.add('is-visible'));
    }

    // Responsive menu.
    const menuToggle = $('#menuToggle');
    const navLinks = $('#navLinks');
    menuToggle.addEventListener('click', () => {
      const open = navLinks.classList.toggle('open');
      menuToggle.setAttribute('aria-expanded', String(open));
      menuToggle.setAttribute('aria-label', open ? 'Tutup menu' : 'Buka menu');
    });
    $$('#navLinks a').forEach((link) => link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      menuToggle.setAttribute('aria-expanded', 'false');
      menuToggle.setAttribute('aria-label', 'Buka menu');
    }));

    // Destination search filters cards in-place.
    const searchInput = $('#packageSearch');
    const cards = $$('.package-card');
    const emptyState = $('#emptyState');
    searchInput.addEventListener('input', () => {
      const query = searchInput.value.trim().toLocaleLowerCase('id');
      let visibleCount = 0;
      cards.forEach((card) => {
        const searchable = `${card.dataset.destination} ${card.dataset.search} ${card.innerText}`.toLocaleLowerCase('id');
        const match = searchable.includes(query);
        card.hidden = !match;
        if (match) visibleCount++;
      });
      emptyState.classList.toggle('show', visibleCount === 0);
      if (query) $('#paket').scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
    });

    // Booking modal.
    const modal = $('#bookingModal');
    const form = $('#bookingForm');
    const result = $('#bookingResult');
    const summaryNode = $('#bookingSummary');
    const copyButton = $('#copyBooking');
    let latestSummary = '';
    const openModal = (destination = '') => {
      modal.classList.add('open');
      modal.setAttribute('aria-hidden', 'false');
      document.body.classList.add('modal-open');
      if (destination) $('#bookingDestination').value = destination;
      result.classList.remove('show');
      window.setTimeout(() => (destination ? $('#bookingDate') : $('#bookingDestination')).focus(), 140);
    };
    const closeModal = () => {
      modal.classList.remove('open');
      modal.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('modal-open');
    };
    $$('[data-book-open]').forEach((button) => button.addEventListener('click', () => openModal(button.dataset.destination || '')));
    $('#closeModal').addEventListener('click', closeModal);
    modal.addEventListener('click', (event) => { if (event.target === modal) closeModal(); });
    document.addEventListener('keydown', (event) => { if (event.key === 'Escape' && modal.classList.contains('open')) closeModal(); });
    $$('.footer-col [data-footer-destination]').forEach((link) => link.addEventListener('click', (event) => {
      event.preventDefault();
      openModal(link.dataset.footerDestination);
    }));
    const today = new Date();
    const localISODate = new Date(today.getTime() - today.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
    $('#bookingDate').min = localISODate;
    $('#yearNow').textContent = new Date().getFullYear();

    form.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const data = new FormData(form);
      const destination = data.get('destination');
      const date = data.get('date');
      const people = data.get('people');
      const name = data.get('name').trim();
      const contact = data.get('contact').trim();
      const formattedDate = new Intl.DateTimeFormat('id-ID', { dateStyle: 'full', timeZone: 'UTC' }).format(new Date(`${date}T12:00:00Z`));
      latestSummary = `Halo RFA Trip, saya ingin menanyakan open trip.\n\nDestinasi: ${destination}\nTanggal pilihan: ${formattedDate}\nJumlah peserta: ${people}\nNama: ${name}\nWhatsApp: ${contact}\n\nMohon info ketersediaan, fasilitas yang termasuk, titik keberangkatan, dan harga final. Terima kasih.`;
      summaryNode.textContent = latestSummary;
      result.classList.add('show');
      copyButton.textContent = 'Salin ringkasan';
      if (WHATSAPP_NUMBER.trim()) {
        const url = `https://wa.me/${WHATSAPP_NUMBER.trim()}?text=${encodeURIComponent(latestSummary)}`;
        window.open(url, '_blank', 'noopener,noreferrer');
      }
      result.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'nearest' });
    });
    copyButton.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(latestSummary);
        copyButton.textContent = 'Tersalin ✓';
      } catch (error) {
        const area = document.createElement('textarea');
        area.value = latestSummary;
        area.setAttribute('readonly', '');
        area.style.position = 'fixed'; area.style.opacity = '0';
        document.body.appendChild(area); area.select();
        const copied = document.execCommand('copy');
        area.remove();
        copyButton.textContent = copied ? 'Tersalin ✓' : 'Salin manual dari ringkasan';
      }
    });

    // FAQ accordion, one open item at a time.
    $$('.faq-item').forEach((item) => {
      const question = $('.faq-question', item);
      question.addEventListener('click', () => {
        const wasOpen = item.classList.contains('open');
        $$('.faq-item').forEach((other) => {
          other.classList.remove('open');
          $('.faq-question', other).setAttribute('aria-expanded', 'false');
        });
        if (!wasOpen) {
          item.classList.add('open');
          question.setAttribute('aria-expanded', 'true');
        }
      });
    });

    // Gallery controls shift the visual emphasis between gallery cards.
    const gallery = $('#galleryGrid');
    const galleryItems = $$('.gallery-item', gallery);
    let galleryIndex = 0;
    const moveGallery = (step) => {
      galleryIndex = (galleryIndex + step + galleryItems.length) % galleryItems.length;
      galleryItems.forEach((item, index) => {
        item.style.order = String((index - galleryIndex + galleryItems.length) % galleryItems.length);
      });
      galleryItems.forEach((item, index) => item.classList.toggle('gallery-active', index === galleryIndex));
    };
    $('#galleryPrev').addEventListener('click', () => moveGallery(-1));
    $('#galleryNext').addEventListener('click', () => moveGallery(1));

    // Gentle pointer parallax on desktop only.
    const hero = $('.hero');
    if (window.matchMedia('(hover: hover) and (pointer: fine)').matches && !reduceMotion) {
      hero.addEventListener('pointermove', (event) => {
        const rect = hero.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - .5;
        const y = (event.clientY - rect.top) / rect.height - .5;
        const image = $('.hero__image', hero);
        image.style.transform = `scale(1.055) translate(${x * -8}px, ${y * -6}px)`;
      });
      hero.addEventListener('pointerleave', () => { $('.hero__image', hero).style.transform = ''; });
    }
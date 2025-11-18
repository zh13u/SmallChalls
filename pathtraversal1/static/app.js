// Theme toggle and small UI interactions
(function(){
  const root = document.documentElement;
  const saved = localStorage.getItem('theme');
  if(saved){
    root.setAttribute('data-theme', saved);
  } else if(window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches){
    root.setAttribute('data-theme', 'light');
  }

  const toggle = document.getElementById('themeToggle');
  if(toggle){
    toggle.addEventListener('click', function(){
      const current = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      root.setAttribute('data-theme', current);
      localStorage.setItem('theme', current);
      toggle.textContent = current === 'light' ? 'Dark' : 'Light';
    });
    // Initialize label
    const current = root.getAttribute('data-theme');
    toggle.textContent = current === 'light' ? 'Dark' : 'Light';
  }

  // Stagger reveal for file cards
  const cards = document.querySelectorAll('.file-card');
  cards.forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(6px)';
    setTimeout(() => {
      el.style.transition = 'opacity .22s ease, transform .22s ease';
      el.style.opacity = '1';
      el.style.transform = 'none';
    }, 40 + i*50);
  });

  // File-type icon enrichment
  const extToEmoji = { txt:'📄', md:'📝', png:'🖼️', jpg:'🖼️', jpeg:'🖼️', gif:'🖼️', pdf:'📕', zip:'🗜️' };
  document.querySelectorAll('.file-card .file-name').forEach(node => {
    const label = node.querySelector('span[title]');
    const ico = node.querySelector('.file-ico');
    if(label && ico){
      const name = (label.getAttribute('title')||'').toLowerCase();
      const ext = name.includes('.') ? name.split('.').pop() : '';
      if(extToEmoji[ext]){ ico.textContent = extToEmoji[ext]; }
    }
  });

  // Upload dropzone enhancement (works on upload page)
  const form = document.querySelector('form[enctype="multipart/form-data"]');
  const fileInput = form ? form.querySelector('input[type="file"]') : null;
  if(form && fileInput){
    // Wrap in dropzone if not present
    let zone = form.querySelector('.dropzone');
    if(!zone){
      zone = document.createElement('div');
      zone.className = 'dropzone';
      zone.innerHTML = '<div>Drag & drop files here or click to choose</div>';
      fileInput.parentNode.insertBefore(zone, fileInput);
      zone.appendChild(fileInput);
    }
    ;['dragenter','dragover'].forEach(evt => zone.addEventListener(evt, e => { e.preventDefault(); e.stopPropagation(); zone.classList.add('drag'); }));
    ;['dragleave','drop'].forEach(evt => zone.addEventListener(evt, e => { e.preventDefault(); e.stopPropagation(); zone.classList.remove('drag'); }));
    zone.addEventListener('drop', e => { if(e.dataTransfer && e.dataTransfer.files){ fileInput.files = e.dataTransfer.files; }});
    zone.addEventListener('click', () => fileInput.click());
  }
})();



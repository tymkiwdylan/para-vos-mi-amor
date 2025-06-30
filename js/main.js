// JavaScript para "Para vos, mi amor" - La carta de amor más hermosa
document.addEventListener('DOMContentLoaded', function() {
  const secciones = document.querySelectorAll('.seccion');
  const instruccion = document.getElementById('instruccion');
  const canvas = document.getElementById('corazones');
  const particleCanvas = document.getElementById('particulas');
  const progressDots = document.querySelectorAll('.progress-dot');
  const ctx = canvas.getContext('2d');
  const particleCtx = particleCanvas.getContext('2d');
  
  // Setup canvas dimensions
  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    particleCanvas.width = window.innerWidth;
    particleCanvas.height = window.innerHeight;
  }
  resizeCanvas();

  let indiceActual = 0;
  let particles = [];
  let isTransitioning = false;

  // Initialize Hammer.js for gestures
  const contenedor = document.getElementById('contenedor');
  const hammer = new Hammer(contenedor);
  hammer.get('swipe').set({ direction: Hammer.DIRECTION_ALL });
  
  // Handle swipe gestures
  hammer.on('swipeleft', () => {
    if (!isTransitioning) {
      avanzarSeccion();
    }
  });
  
  hammer.on('swiperight', () => {
    if (!isTransitioning) {
      retrocederSeccion();
    }
  });
  
  // Handle tap for forward navigation
  hammer.on('tap', () => {
    if (!isTransitioning) {
      avanzarSeccion();
    }
  });

  // Enhanced keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (!isTransitioning) {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {
        avanzarSeccion();
      } else if (e.key === 'ArrowLeft' || e.key === 'Backspace') {
        retrocederSeccion();
      }
    }
  });

  // Initialize particles
  function initParticles() {
    particles = [];
    for (let i = 0; i < 50; i++) {
      particles.push({
        x: Math.random() * particleCanvas.width,
        y: Math.random() * particleCanvas.height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        size: Math.random() * 2 + 1,
        opacity: Math.random() * 0.5 + 0.2,
        life: Math.random() * 100
      });
    }
  }

  // Animate particles
  function animateParticles() {
    particleCtx.clearRect(0, 0, particleCanvas.width, particleCanvas.height);
    
    particles.forEach((particle, index) => {
      particle.x += particle.vx;
      particle.y += particle.vy;
      particle.life += 0.5;
      
      // Wrap around screen
      if (particle.x < 0) particle.x = particleCanvas.width;
      if (particle.x > particleCanvas.width) particle.x = 0;
      if (particle.y < 0) particle.y = particleCanvas.height;
      if (particle.y > particleCanvas.height) particle.y = 0;
      
      // Create sparkle effect
      const alpha = Math.sin(particle.life * 0.1) * 0.5 + 0.5;
      particleCtx.beginPath();
      particleCtx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
      particleCtx.fillStyle = `rgba(177, 156, 217, ${alpha * particle.opacity})`;
      particleCtx.fill();
      
      // Add twinkle effect
      if (Math.random() < 0.1) {
        particleCtx.beginPath();
        particleCtx.arc(particle.x, particle.y, particle.size * 2, 0, Math.PI * 2);
        particleCtx.fillStyle = `rgba(255, 255, 255, ${alpha * 0.3})`;
        particleCtx.fill();
      }
    });
    
    requestAnimationFrame(animateParticles);
  }

  // Update progress indicator
  function updateProgress(index) {
    progressDots.forEach((dot, i) => {
      dot.classList.toggle('active', i === index);
    });
  }

  // Enhanced section animation with bidirectional support
  function animarSeccion(indice, direccion = 'forward') {
    if (indice < secciones.length) {
      isTransitioning = true;
      const seccion = secciones[indice];
      const content = seccion.querySelector('.seccion-content');
      
      // Hide all other sections
      secciones.forEach((sec, i) => {
        if (i !== indice && sec.style.display !== 'none') {
          const isGoingForward = direccion === 'forward';
          anime({
            targets: sec,
            opacity: 0,
            scale: 0.95,
            rotateY: isGoingForward ? -15 : 15,
            duration: 600,
            easing: 'easeInQuart',
            complete: () => {
              sec.style.display = 'none';
            }
          });
        }
      });
      
      // Show current section
      seccion.style.display = 'flex';
      seccion.style.opacity = 0;
      
      // Determine animation direction
      const isGoingForward = direccion === 'forward';
      const enterRotation = isGoingForward ? 15 : -15;
      const enterTranslateY = isGoingForward ? 50 : -50;
      
      // Animate section entrance
      anime({
        targets: seccion,
        opacity: [0, 1],
        translateY: [enterTranslateY, 0],
        rotateY: [enterRotation, 0],
        duration: 800,
        easing: 'easeOutQuart',
        begin: () => {
          updateProgress(indice);
        }
      });
      
      // Animate content with stagger
      anime({
        targets: content,
        scale: [0.8, 1],
        opacity: [0, 1],
        translateY: [30, 0],
        duration: 1000,
        easing: 'easeOutBack',
        delay: 300,
        complete: () => {
          isTransitioning = false;
          
          // Add random floating hearts for romantic effect
          if (Math.random() < 0.7) {
            createFloatingHearts(3);
          }
        }
      });
      
      // Animate text elements separately for extra effect
      const textElements = content.querySelectorAll('h1, p');
      anime({
        targets: textElements,
        translateY: [20, 0],
        opacity: [0, 1],
        duration: 800,
        delay: anime.stagger(200, { start: 500 }),
        easing: 'easeOutQuart'
      });
      
    } else {
      // Final hearts animation
      instruccion.style.display = 'none';
      mostrarCorazonesFinal();
    }
  }

  // Create floating hearts during transitions
  function createFloatingHearts(count = 5) {
    const hearts = [];
    for (let i = 0; i < count; i++) {
      hearts.push({
        x: Math.random() * canvas.width,
        y: canvas.height + 50,
        size: Math.random() * 20 + 15,
        speed: Math.random() * 3 + 2,
        drift: (Math.random() - 0.5) * 2,
        rotation: Math.random() * 360,
        opacity: Math.random() * 0.7 + 0.3
      });
    }

    const animateHeart = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      hearts.forEach((heart, index) => {
        heart.y -= heart.speed;
        heart.x += heart.drift;
        heart.rotation += 2;
        
        if (heart.y < -50) {
          hearts.splice(index, 1);
          return;
        }
        
        ctx.save();
        ctx.translate(heart.x, heart.y);
        ctx.rotate(heart.rotation * Math.PI / 180);
        ctx.scale(heart.size / 20, heart.size / 20);
        
        // Draw heart with gradient
        const gradient = ctx.createRadialGradient(0, 0, 0, 0, 0, 20);
        gradient.addColorStop(0, `rgba(255, 107, 157, ${heart.opacity})`);
        gradient.addColorStop(1, `rgba(255, 164, 196, ${heart.opacity * 0.5})`);
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.moveTo(0, 3);
        ctx.bezierCurveTo(0, 0, -5, -2, -5, -6);
        ctx.bezierCurveTo(-5, -10, 0, -8, 0, -4);
        ctx.bezierCurveTo(0, -8, 5, -10, 5, -6);
        ctx.bezierCurveTo(5, -2, 0, 0, 0, 3);
        ctx.fill();
        
        ctx.restore();
      });
      
      if (hearts.length > 0) {
        requestAnimationFrame(animateHeart);
      }
    };
    
    animateHeart();
  }

  // Enhanced final hearts animation
  function mostrarCorazonesFinal() {
    isTransitioning = true;
    const finalHearts = [];
    
    // Create spectacular heart shower
    for (let i = 0; i < 30; i++) {
      finalHearts.push({
        x: Math.random() * canvas.width,
        y: canvas.height + Math.random() * 200,
        speed: Math.random() * 4 + 2,
        size: Math.random() * 25 + 20,
        rotation: Math.random() * 360,
        drift: (Math.random() - 0.5) * 3,
        color: `hsl(${Math.random() * 60 + 300}, 70%, ${Math.random() * 30 + 60}%)`
      });
    }

    const animateHeartsShower = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      finalHearts.forEach((heart) => {
        heart.y -= heart.speed;
        heart.x += Math.sin(heart.y * 0.01) * heart.drift;
        heart.rotation += 3;
        
        ctx.save();
        ctx.translate(heart.x, heart.y);
        ctx.rotate(heart.rotation * Math.PI / 180);
        ctx.scale(heart.size / 20, heart.size / 20);
        
        // Enhanced heart drawing with glow effect
        ctx.shadowColor = heart.color;
        ctx.shadowBlur = 10;
        ctx.fillStyle = heart.color;
        
        ctx.beginPath();
        ctx.moveTo(0, 6);
        ctx.bezierCurveTo(0, 2, -8, -2, -8, -8);
        ctx.bezierCurveTo(-8, -14, 0, -10, 0, -6);
        ctx.bezierCurveTo(0, -10, 8, -14, 8, -8);
        ctx.bezierCurveTo(8, -2, 0, 2, 0, 6);
        ctx.fill();
        
        ctx.restore();
      });
      
      // Continue animation if hearts are still visible
      if (finalHearts.some(heart => heart.y > -100)) {
        requestAnimationFrame(animateHeartsShower);
      } else {
        mostrarMensajeFinal();
      }
    };
    
    animateHeartsShower();
  }

  // Enhanced final message
  function mostrarMensajeFinal() {
    // Hide progress indicator
    anime({
      targets: '.progress-container',
      opacity: 0,
      translateY: -20,
      duration: 500
    });
    
    const mensajeFinal = document.createElement('div');
    mensajeFinal.className = 'mensaje-final';
    mensajeFinal.innerHTML = `
      <h1>Te amo</h1>
      <p style="margin-top: 20px; font-size: 1.8em;">Con todo mi corazón,</p>
      <p style="margin-top: 10px; font-size: 2.2em; color: #b19cd9;">Dylan 💕</p>
    `;
    
    contenedor.appendChild(mensajeFinal);
    
    // Animate final message appearance
    anime({
      targets: mensajeFinal,
      opacity: [0, 1],
      scale: [0.5, 1],
      rotateY: [90, 0],
      duration: 1500,
      easing: 'easeOutBack',
      complete: () => {
        // Add celebration effect
        createCelebrationEffect();
        isTransitioning = false;
      }
    });
  }

  // Celebration particle explosion
  function createCelebrationEffect() {
    const celebrationParticles = [];
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    
    for (let i = 0; i < 100; i++) {
      const angle = (Math.PI * 2 * i) / 100;
      celebrationParticles.push({
        x: centerX,
        y: centerY,
        vx: Math.cos(angle) * (Math.random() * 8 + 2),
        vy: Math.sin(angle) * (Math.random() * 8 + 2),
        life: 0,
        maxLife: Math.random() * 60 + 60,
        size: Math.random() * 4 + 2,
        color: `hsl(${Math.random() * 60 + 300}, 80%, 70%)`
      });
    }
    
    const animateCelebration = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      celebrationParticles.forEach((particle, index) => {
        particle.x += particle.vx;
        particle.y += particle.vy;
        particle.vy += 0.1; // gravity
        particle.life++;
        
        const alpha = 1 - (particle.life / particle.maxLife);
        
        if (particle.life < particle.maxLife && alpha > 0) {
          ctx.save();
          ctx.globalAlpha = alpha;
          ctx.fillStyle = particle.color;
          ctx.beginPath();
          ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();
        } else {
          celebrationParticles.splice(index, 1);
        }
      });
      
      if (celebrationParticles.length > 0) {
        requestAnimationFrame(animateCelebration);
      }
    };
    
    animateCelebration();
  }

  // Advance to next section
  function avanzarSeccion() {
    if (indiceActual < secciones.length) {
      if (indiceActual < secciones.length - 1) {
        indiceActual++;
      } else {
        indiceActual++;
      }
      animarSeccion(indiceActual, 'forward');
    }
  }

  // Go back to previous section
  function retrocederSeccion() {
    if (indiceActual > 0) {
      indiceActual--;
      animarSeccion(indiceActual, 'backward');
    }
  }

  // Navigate to specific section
  function irASeccion(targetIndex) {
    if (targetIndex >= 0 && targetIndex < secciones.length && targetIndex !== indiceActual) {
      const direccion = targetIndex > indiceActual ? 'forward' : 'backward';
      indiceActual = targetIndex;
      animarSeccion(indiceActual, direccion);
    }
  }

  // Initialize everything
  initParticles();
  animateParticles();
  
  // Hide all sections except first
  secciones.forEach((seccion, i) => {
    if (i !== 0) seccion.style.display = 'none';
  });
  
  // Animate first section and instruction
  animarSeccion(0, 'forward');
  anime({
    targets: instruccion,
    opacity: [0, 1],
    translateY: [20, 0],
    delay: 2000,
    duration: 1000,
    easing: 'easeOutQuad'
  });

  // Handle window resize
  window.addEventListener('resize', resizeCanvas);
  
  // Add click handlers to progress dots for direct navigation
  progressDots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      if (!isTransitioning) {
        irASeccion(index);
      }
    });
  });
});


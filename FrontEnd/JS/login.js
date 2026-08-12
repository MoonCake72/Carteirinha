document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');
  const emailInput = document.getElementById('email');
  const senhaInput = document.getElementById('senha');
  const errorMsg = document.getElementById('error-msg');
  const submitBtn = document.getElementById('submit-btn');
  const toggleEye = document.getElementById('toggle-eye');
  const loginBlock = document.getElementById('login-block');
  const successBlock = document.getElementById('success-block');
  const forgotLink = document.getElementById('forgot-link');
  const signupBtn = document.getElementById('signup-btn');

  // Ícones SVG Lucide (Linha perfeita e consistente)
  const eyeOpenSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>`;
  const eyeClosedSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.52 13.52 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><line x1="2" x2="22" y1="2" y2="22"/></svg>`;

  // Inicializa o botão com o ícone padrão
  if (toggleEye) {
    toggleEye.innerHTML = eyeOpenSVG;

    toggleEye.addEventListener('click', () => {
      const isPassword = senhaInput.type === 'password';
      senhaInput.type = isPassword ? 'text' : 'password';
      toggleEye.innerHTML = isPassword ? eyeClosedSVG : eyeOpenSVG;
    });
  }

  // Validação e Envio do Formulário
  // Validação e Envio do Formulário para a API
  form.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    errorMsg.textContent = '';

    const email = emailInput.value.trim();
    const password = senhaInput.value;

    if (!email || !password) {
      errorMsg.textContent = 'preencha e-mail e senha pra continuar';
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Entrando...';

    try {
      // Faz a requisição POST para a API FastAPI
      const response = await fetch('https://carteirinha-api.onrender.com/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Falha ao realizar login');
      }

      // Salva o Token JWT e o nome do tutor no navegador para manter a sessão
      localStorage.setItem('pet_token', data.access_token);
      localStorage.setItem('tutor_name', data.user_name);

      // Exibe tela de sucesso e redireciona para a carteirinha
      loginBlock.classList.add('hidden');
      successBlock.classList.remove('hidden');

      setTimeout(() => {
        window.location.href = 'index.html';
      }, 900);

    } catch (error) {
      errorMsg.textContent = error.message;
      submitBtn.disabled = false;
      submitBtn.textContent = 'Entrar 🐾';
    }
  });

  // Links auxiliares
  forgotLink.addEventListener('click', () => {
    errorMsg.textContent = 'envie um e-mail pra gente redefinir sua senha 💌';
  });

  // Redireciona para a tela de cadastro ao clicar no botão
  signupBtn.addEventListener('click', () => {
    window.location.href = 'register.html';
  });
});
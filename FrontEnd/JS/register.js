document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('register-form');
  const nomeInput = document.getElementById('nome');
  const emailInput = document.getElementById('email');
  const senhaInput = document.getElementById('senha');
  const confirmSenhaInput = document.getElementById('confirmar-senha');
  const errorMsg = document.getElementById('error-msg');
  const submitBtn = document.getElementById('submit-btn');
  const loginBlock = document.getElementById('login-block');
  const successBlock = document.getElementById('success-block');

  // SVGs de Olho (Lucide)
  const eyeOpenSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>`;
  const eyeClosedSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.52 13.52 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><line x1="2" x2="22" y1="2" y2="22"/></svg>`;

  // Função para configurar os botões de ver senha
  function setupEyeToggle(buttonId, inputElement) {
    const btn = document.getElementById(buttonId);
    if (btn) {
      btn.innerHTML = eyeOpenSVG;
      btn.addEventListener('click', () => {
        const isPassword = inputElement.type === 'password';
        inputElement.type = isPassword ? 'text' : 'password';
        btn.innerHTML = isPassword ? eyeClosedSVG : eyeOpenSVG;
      });
    }
  }

  setupEyeToggle('toggle-eye-1', senhaInput);
  setupEyeToggle('toggle-eye-2', confirmSenhaInput);

  // Envio de Cadastro para a API
  form.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    errorMsg.textContent = '';

    const name = nomeInput.value.trim();
    const email = emailInput.value.trim();
    const password = senhaInput.value;
    const confirmPassword = confirmSenhaInput.value;

    if (!name || !email || !password || !confirmPassword) {
      errorMsg.textContent = 'preencha todos os campos pra continuar';
      return;
    }

    if (password.length < 4) {
      errorMsg.textContent = 'a senha precisa ter pelo menos 4 caracteres';
      return;
    }

    if (password !== confirmPassword) {
      errorMsg.textContent = 'as senhas não coincidem!';
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Criando conta...';

    try {
      // Para testes locais const response = await fetch('http://127.0.0.1:8000/api/auth/register'. 
      // Em produção no Render,const response = await fetch('https://carteirinha-api.onrender.com/api/auth/register'
      const response = await fetch('https://carteirinha-api.onrender.com/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email, password })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Erro ao criar conta');
      }

      // Exibe feedback de sucesso e envia o usuário para o login
      loginBlock.classList.add('hidden');
      successBlock.classList.remove('hidden');

      setTimeout(() => {
        window.location.href = 'login.html';
      }, 1200);

    } catch (error) {
      errorMsg.textContent = error.message;
      submitBtn.disabled = false;
      submitBtn.textContent = 'Cadastrar 🐾';
    }
  });
});
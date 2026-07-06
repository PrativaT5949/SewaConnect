
    const togglePass = document.getElementById('togglePass');
    const passInput = document.getElementById('passInput');
    togglePass.addEventListener('click', () => {
      passInput.type = passInput.type === 'password' ? 'text' : 'password';
    });

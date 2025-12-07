document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Dark Mode Logic
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    
    if (localStorage.getItem('theme') === 'light') {
        body.classList.add('light-mode');
        if(themeToggle) themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            body.classList.toggle('light-mode');
            if (body.classList.contains('light-mode')) {
                localStorage.setItem('theme', 'light');
                themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            } else {
                localStorage.setItem('theme', 'dark');
                themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            }
        });
    }

    // 2. Password Strength Meter
    const passInput = document.getElementById('reg_pass');
    const meter = document.querySelector('.strength-meter');
    
    if (passInput && meter) {
        passInput.addEventListener('input', function() {
            const val = this.value;
            let strength = 0;
            if (val.length >= 8) strength++;
            if (val.match(/[A-Z]/)) strength++;
            if (val.match(/[0-9]/)) strength++;
            if (val.match(/[^a-zA-Z0-9]/)) strength++;

            meter.className = 'strength-meter'; // Reset
            if (strength > 3) meter.classList.add('strength-strong');
            else if (strength > 1) meter.classList.add('strength-medium');
            else if (val.length > 0) meter.classList.add('strength-weak');
        });
    }

    // 3. Auto Hide Alerts
    setTimeout(() => {
        const alerts = document.querySelectorAll('.flash');
        alerts.forEach(a => a.style.display = 'none');
    }, 4000);
});

// 4. Toggle Password Visibility
function togglePass(id) {
    const input = document.getElementById(id);
    const icon = document.querySelector(`[onclick="togglePass('${id}')"]`);
    
    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = "password";
        icon.classList.remove('fa-eye'); // Reset to default eye if needed
        icon.classList.add('fa-eye');
    }
}
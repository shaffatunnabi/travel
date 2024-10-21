let users = [];

function clearErrors() {
    document.getElementById('username-error').textContent = '';
    document.getElementById('email-error').textContent = '';
    document.getElementById('password-error').textContent = '';
    document.getElementById('confirm-password-error').textContent = '';
    document.getElementById('age-error').textContent = '';
}

function validateSignup() {
    clearErrors(); // Clear previous error messages

    const username = document.getElementById('signup-username').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('signup-confirm-password').value;
    const age = document.getElementById('signup-age').value;

    let isValid = true;

    // Username validation (3 to 20 characters)
    if (username.length < 3 || username.length > 20) {
        document.getElementById('username-error').textContent = 'Username must be between 3 and 20 characters.';
        isValid = false;
    }

    // Username validation (alphanumeric)
    if (!/^[a-zA-Z0-9]+$/.test(username)) {
        document.getElementById('username-error').textContent = 'Username must be alphanumeric.';
        isValid = false;
    }

    // Email validation
    const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    if (!emailValid) {
        document.getElementById('email-error').textContent = 'Please enter a valid email address.';
        isValid = false;
    }

    // Check for existing username
    if (users.some(user => user.username === username)) {
        document.getElementById('username-error').textContent = 'Username already exists!';
        isValid = false;
    }

    // Password validation (must contain at least one capital letter, one number, and one letter)
    const passwordValid = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[A-Z]).{8,}$/.test(password);
    if (!passwordValid) {
        document.getElementById('password-error').textContent = 'Password must contain at least one letter, one number, one capital letter, and be at least 8 characters long.';
        isValid = false;
    }

    // Check if passwords match
    if (password !== confirmPassword) {
        document.getElementById('confirm-password-error').textContent = 'Passwords do not match!';
        isValid = false;
    }

    // Check age (must be 18 or older)
    if (age < 18) {
        document.getElementById('age-error').textContent = 'You must be at least 18 years old to create an account.';
        isValid = false;
    }

    // Add new user if valid
    if (isValid) {
        users.push({ username, email, password, age });
        alert('Signup successful!');
    }

    return false; // Prevent form submission
}

function validateLogin() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const messageElement = document.getElementById('login-message');

    const user = users.find(user => user.username === username && user.password === password);

    if (!user) {
        messageElement.textContent = 'Invalid username or password!';
        return false;
    }

    messageElement.textContent = 'Login successful!';
    return false; // Prevent form submission
}

function showSignup() {
    window.location.href = 'signup.html'; // Redirect to signup page
}

function showLogin() {
    window.location.href = 'login.html'; // Redirect to login page
}

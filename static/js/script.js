document.addEventListener('DOMContentLoaded', function() {
    // Navigation
    const navLinks = document.querySelectorAll('nav a');
    const sections = {
        dashboard: document.getElementById('dashboard'),
        users: document.getElementById('users'),
        emails: document.getElementById('emails')
    };
    const pageTitle = document.getElementById('page-title');

    // User Management
    const btnAddUser = document.getElementById('btn-add-user');
    const addUserForm = document.getElementById('add-user-form');
    const formUser = document.getElementById('form-user');
    const btnCancelAdd = document.getElementById('btn-cancel-add');
    const usersTableBody = document.getElementById('users-table-body');

    // Email Management
    const emailsTableBody = document.getElementById('emails-table-body');
    const btnRefreshEmails = document.getElementById('btn-refresh-emails');

    // Actions
    const btnGenerateUsers = document.getElementById('btn-generate-users');
    const btnGenerateEmails = document.getElementById('btn-generate-emails');
    const btnMassGenerate = document.getElementById('btn-mass-generate');
    const massUsersCount = document.getElementById('mass-users-count');
    const btnClearUsers = document.getElementById('btn-clear-users');
    const btnClearEmails = document.getElementById('btn-clear-emails');

    // Stats
    const totalUsersCount = document.getElementById('total-users-count');
    const totalEmailsCount = document.getElementById('total-emails-count');
    const providersCount = document.getElementById('providers-count');
    const usersGrowth = document.getElementById('users-growth');
    const emailsGrowth = document.getElementById('emails-growth');

    // Progress Modal
    const progressModal = document.getElementById('progress-modal');
    const progressTitle = document.getElementById('progress-title');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const progressPercent = document.getElementById('progress-percent');

    // Message Toast
    const messageToast = document.getElementById('message-toast');
    const toastIcon = document.getElementById('toast-icon');
    const toastMessage = document.getElementById('toast-message');

    // Initialize
    initNavigation();
    loadDashboardData();
    loadUsers();
    loadEmails();

    // Navigation Functions
    function initNavigation() {
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const target = this.getAttribute('href').substring(1);
                
                // Update active nav link
                navLinks.forEach(nav => {
                    nav.classList.remove('bg-primary/20', 'text-primary');
                    nav.classList.add('text-text-secondary-dark', 'hover:bg-surface-dark', 'hover:text-text-primary-dark');
                });
                this.classList.remove('text-text-secondary-dark', 'hover:bg-surface-dark', 'hover:text-text-primary-dark');
                this.classList.add('bg-primary/20', 'text-primary');
                
                // Show target section
                Object.values(sections).forEach(section => section.classList.add('hidden'));
                if (sections[target]) {
                    sections[target].classList.remove('hidden');
                }
                
                // Update page title
                updatePageTitle(target);
            });
        });
    }

    function updatePageTitle(section) {
        const titles = {
            dashboard: 'Dashboard Overview',
            users: 'User Management',
            emails: 'Email Management'
        };
        pageTitle.textContent = titles[section] || 'CRM Dashboard';
    }

    // User Management Functions
    btnAddUser.addEventListener('click', function() {
        addUserForm.classList.toggle('hidden');
    });

    btnCancelAdd.addEventListener('click', function() {
        addUserForm.classList.add('hidden');
        formUser.reset();
    });

    formUser.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const userData = {
            nombre: document.getElementById('user-firstname').value,
            apellido: document.getElementById('user-lastname').value,
            edad: parseInt(document.getElementById('user-age').value)
        };
        
        if (!userData.nombre || !userData.apellido || !userData.edad) {
            showMessage('All fields are required', 'error');
            return;
        }
        
        fetch('/usuarios', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error || 'Network error'); });
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                showMessage('Error: ' + data.error, 'error');
            } else {
                formUser.reset();
                addUserForm.classList.add('hidden');
                loadUsers();
                loadDashboardData();
                showMessage('User added successfully', 'success');
            }
        })
        .catch(error => {
            console.error('Error adding user:', error);
            showMessage('Error adding user: ' + error.message, 'error');
        });
    });

    function loadUsers() {
        console.log("Loading users...");
        fetch('/usuarios')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(users => {
                console.log("Users loaded:", users);
                usersTableBody.innerHTML = '';
                
                if (!users || users.length === 0) {
                    usersTableBody.innerHTML = `
                        <tr>
                            <td colspan="6" class="px-4 py-8 text-center text-text-secondary-dark">
                                No users found
                            </td>
                        </tr>
                    `;
                    return;
                }
                
                // Check if users is an array
                if (!Array.isArray(users)) {
                    console.error('Expected array but got:', users);
                    usersTableBody.innerHTML = `
                        <tr>
                            <td colspan="6" class="px-4 py-8 text-center text-red-400">
                                Error: Invalid data format
                            </td>
                        </tr>
                    `;
                    return;
                }
                
                users.forEach(user => {
                    const fecha = user.fecha_creacion ? new Date(user.fecha_creacion).toLocaleDateString() : 'N/A';
                    const row = document.createElement('tr');
                    row.className = 'border-t border-t-border-dark/50 hover:bg-background-dark/50';
                    row.innerHTML = `
                        <td class="h-[72px] px-4 py-2 text-text-secondary-dark text-sm font-normal">${user.id}</td>
                        <td class="h-[72px] px-4 py-2 text-text-secondary-dark text-sm font-normal">${user.nombre}</td>
                        <td class="h-[72px] px-4 py-2 text-text-secondary-dark text-sm font-normal">${user.apellido}</td>
                        <td class="h-[72px] px-4 py-2 text-text-secondary-dark text-sm font-normal">${user.edad}</td>
                        <td class="h-[72px] px-4 py-2 text-text-secondary-dark text-sm font-normal">${fecha}</td>
                        <td class="h-[72px] px-4 py-2">
                            <button onclick="deleteUser(${user.id})" class="text-red-400 text-sm font-medium hover:text-red-300 transition-colors">
                                Delete
                            </button>
                        </td>
                    `;
                    usersTableBody.appendChild(row);
                });
            })
            .catch(error => {
                console.error('Error loading users:', error);
                usersTableBody.innerHTML = `
                    <tr>
                        <td colspan="6" class="px-4 py-8 text-center text-red-400">
                            Error loading users: ${error.message}
                        </td>
                    </tr>
                `;
            });
    }

    // Email Management Functions
    btnRefreshEmails.addEventListener('click', loadEmails);

    function loadEmails() {
        console.log("Loading emails...");
        fetch('/correos')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(emails => {
                console.log("Emails loaded:", emails);
                emailsTableBody.innerHTML = '';
                
                if (!emails || emails.length === 0) {
                    emailsTableBody.innerHTML = `
                        <tr>
                            <td colspan="4" class="px-4 py-8 text-center text-text-secondary-dark">
                                No emails generated yet
                            </td>
                        </tr>
                    `;
                    return;
                }
                
                if (!Array.isArray(emails)) {
                    console.error('Expected array but got:', emails);
                    emailsTableBody.innerHTML = `
                        <tr>
                            <td colspan="4" class="px-4 py-8 text-center text-red-400">
                                Error: Invalid data format
                            </td>
                        </tr>
                    `;
                    return;
                }
                
                emails.forEach(email => {
                    const fecha = email.fecha_creacion ? new Date(email.fecha_creacion).toLocaleString() : 'N/A';
                    const row = document.createElement('tr');
                    row.className = 'border-t border-t-border-dark/50 hover:bg-background-dark/50';
                    row.innerHTML = `
                        <td class="h-[72px] px-4 py-2 text-text-secondary-dark text-sm">${email.nombre} ${email.apellido}</td>
                        <td class="h-[72px] px-4 py-2">
                            <span class="badge badge-${email.tipo}">${email.tipo}</span>
                        </td>
                        <td class="h-[72px] px-4 py-2 text-text-secondary-dark text-sm">${email.correo}</td>
                        <td class="h-[72px] px-4 py-2 text-text-secondary-dark text-sm">${fecha}</td>
                    `;
                    emailsTableBody.appendChild(row);
                });
            })
            .catch(error => {
                console.error('Error loading emails:', error);
                emailsTableBody.innerHTML = `
                    <tr>
                        <td colspan="4" class="px-4 py-8 text-center text-red-400">
                            Error loading emails: ${error.message}
                        </td>
                    </tr>
                `;
            });
    }

    // Action Functions
    btnGenerateUsers.addEventListener('click', function() {
        const count = 100; // Default count for quick action
        generateRandomUsers(count);
    });

    btnMassGenerate.addEventListener('click', function() {
        const count = parseInt(massUsersCount.value) || 1000;
        if (count > 10000) {
            showMessage('Maximum allowed is 10,000 users', 'error');
            return;
        }
        generateRandomUsers(count);
    });

    btnGenerateEmails.addEventListener('click', generateEmailsConcurrent);

    btnClearUsers.addEventListener('click', function() {
        if (confirm('Are you sure you want to delete ALL users? This action cannot be undone.')) {
            fetch('/usuarios/todos', {
                method: 'DELETE'
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.error || 'Network error'); });
                }
                return response.json();
            })
            .then(data => {
                loadUsers();
                loadEmails();
                loadDashboardData();
                showMessage('All users deleted successfully', 'success');
            })
            .catch(error => {
                console.error('Error deleting users:', error);
                showMessage('Error deleting users: ' + error.message, 'error');
            });
        }
    });

    btnClearEmails.addEventListener('click', function() {
        if (confirm('Are you sure you want to delete ALL emails?')) {
            fetch('/correos/todos', {
                method: 'DELETE'
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.error || 'Network error'); });
                }
                return response.json();
            })
            .then(data => {
                loadEmails();
                loadDashboardData();
                showMessage('All emails deleted successfully', 'success');
            })
            .catch(error => {
                console.error('Error deleting emails:', error);
                showMessage('Error deleting emails: ' + error.message, 'error');
            });
        }
    });

    function generateRandomUsers(count) {
        console.log(`Generating ${count} random users...`);
        showProgress('Generating random users...', 0);
        
        fetch('/usuarios/aleatorios', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cantidad: count })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error || 'Network error'); });
            }
            return response.json();
        })
        .then(data => {
            console.log("Users generation response:", data);
            if (data.error) {
                throw new Error(data.error);
            }
            updateProgress('Completed!', 100);
            setTimeout(() => {
                hideProgress();
                loadUsers();
                loadDashboardData();
                showMessage(`Generated ${data.usuarios ? data.usuarios.length : 0} random users`, 'success');
            }, 500);
        })
        .catch(error => {
            console.error('Error generating users:', error);
            hideProgress();
            showMessage('Error generating users: ' + error.message, 'error');
        });
    }

    function generateEmailsConcurrent() {
        console.log("Generating emails concurrently...");
        showProgress('Generating emails concurrently...', 0);
        
        // Simulate progress
        let progress = 0;
        const interval = setInterval(() => {
            progress += 5;
            if (progress <= 90) {
                updateProgress('Generating emails...', progress);
            }
        }, 200);
        
        fetch('/generar-correos', {
            method: 'POST'
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error || 'Network error'); });
            }
            return response.json();
        })
        .then(data => {
            clearInterval(interval);
            console.log("Emails generation response:", data);
            
            if (data.error) {
                throw new Error(data.error);
            }
            updateProgress('Completed!', 100);
            setTimeout(() => {
                hideProgress();
                loadEmails();
                loadDashboardData();
                showMessage(`Generated ${data.correos ? data.correos.length : 0} email addresses`, 'success');
            }, 500);
        })
        .catch(error => {
            clearInterval(interval);
            console.error('Error generating emails:', error);
            hideProgress();
            showMessage('Error generating emails: ' + error.message, 'error');
        });
    }

    // Dashboard Functions
    function loadDashboardData() {
        // Load users count
        fetch('/usuarios')
            .then(response => response.json())
            .then(users => {
                if (Array.isArray(users)) {
                    totalUsersCount.textContent = users.length;
                    usersGrowth.textContent = `+${users.length}`;
                }
            })
            .catch(error => {
                console.error('Error loading users count:', error);
            });
        
        // Load emails count
        fetch('/correos')
            .then(response => response.json())
            .then(emails => {
                if (Array.isArray(emails)) {
                    totalEmailsCount.textContent = emails.length;
                    emailsGrowth.textContent = `+${emails.length}`;
                }
            })
            .catch(error => {
                console.error('Error loading emails count:', error);
            });
    }

    // Progress Modal Functions
    function showProgress(title, percentage) {
        progressTitle.textContent = title;
        updateProgress('Starting...', percentage);
        progressModal.classList.remove('hidden');
    }

    function updateProgress(text, percentage) {
        progressText.textContent = text;
        progressPercent.textContent = percentage + '%';
        progressBar.style.width = percentage + '%';
    }

    function hideProgress() {
        progressModal.classList.add('hidden');
    }

    // Message Toast Functions
    function showMessage(message, type) {
        const types = {
            success: { bg: 'bg-green-500/20', border: 'border-green-500/30', icon: 'check_circle', text: 'text-green-400' },
            error: { bg: 'bg-red-500/20', border: 'border-red-500/30', icon: 'error', text: 'text-red-400' },
            info: { bg: 'bg-blue-500/20', border: 'border-blue-500/30', icon: 'info', text: 'text-blue-400' },
            warning: { bg: 'bg-yellow-500/20', border: 'border-yellow-500/30', icon: 'warning', text: 'text-yellow-400' }
        };
        
        const config = types[type] || types.info;
        
        messageToast.className = `fixed top-4 right-4 p-4 rounded-lg z-50 transition-opacity duration-300 ${config.bg} ${config.border} border ${config.text} fade-in`;
        toastIcon.textContent = config.icon;
        toastMessage.textContent = message;
        
        messageToast.classList.remove('hidden');
        
        setTimeout(() => {
            messageToast.classList.add('hidden');
        }, 5000);
    }

    // Global functions
    window.deleteUser = function(id) {
        if (confirm('Are you sure you want to delete this user?')) {
            fetch(`/usuarios/${id}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.error || 'Network error'); });
                }
                return response.json();
            })
            .then(data => {
                loadUsers();
                loadEmails();
                loadDashboardData();
                showMessage('User deleted successfully', 'success');
            })
            .catch(error => {
                console.error('Error deleting user:', error);
                showMessage('Error deleting user: ' + error.message, 'error');
            });
        }
    };
});
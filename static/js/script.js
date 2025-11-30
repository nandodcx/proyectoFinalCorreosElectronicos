document.addEventListener('DOMContentLoaded', function() {
    // Navegación
    const navLinks = document.querySelectorAll('nav a');
    const sections = {
        dashboard: document.getElementById('dashboard'),
        users: document.getElementById('users'),
        emails: document.getElementById('emails')
    };
    const pageTitle = document.getElementById('page-title');

    // Gestión de Usuarios
    const btnAddUser = document.getElementById('btn-add-user');
    const addUserForm = document.getElementById('add-user-form');
    const formUser = document.getElementById('form-user');
    const btnCancelAdd = document.getElementById('btn-cancel-add');
    const usersTableBody = document.getElementById('users-table-body');

    // Gestión de Correos
    const emailsTableBody = document.getElementById('emails-table-body');
    const btnRefreshEmails = document.getElementById('btn-refresh-emails');

    // Acciones
    const btnGenerateUsers = document.getElementById('btn-generate-users');
    const btnGenerateEmails = document.getElementById('btn-generate-emails');
    const btnMassGenerate = document.getElementById('btn-mass-generate');
    const massUsersCount = document.getElementById('mass-users-count');
    const btnClearUsers = document.getElementById('btn-clear-users');
    const btnClearEmails = document.getElementById('btn-clear-emails');

    // Nuevos elementos para selección de tipos de correo
    const btnGenerateSelectedEmails = document.getElementById('btn-generate-selected-emails');
    const emailTypesModal = document.getElementById('email-types-modal');
    const btnGenerateSelected = document.getElementById('btn-generate-selected');
    const btnCancelSelection = document.getElementById('btn-cancel-selection');

    // Filtros
    const searchUsers = document.getElementById('search-users');
    const filterAge = document.getElementById('filter-age');
    const filterSort = document.getElementById('filter-sort');
    const searchEmails = document.getElementById('search-emails');
    const filterProvider = document.getElementById('filter-provider');
    const filterSortEmails = document.getElementById('filter-sort-emails');

    // Estadísticas
    const totalUsersCount = document.getElementById('total-users-count');
    const totalEmailsCount = document.getElementById('total-emails-count');
    const providersCount = document.getElementById('providers-count');
    const usersGrowth = document.getElementById('users-growth');
    const emailsGrowth = document.getElementById('emails-growth');

    // Modal de Progreso
    const progressModal = document.getElementById('progress-modal');
    const progressTitle = document.getElementById('progress-title');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const progressPercent = document.getElementById('progress-percent');

    // Mensaje Toast
    const messageToast = document.getElementById('message-toast');
    const toastIcon = document.getElementById('toast-icon');
    const toastMessage = document.getElementById('toast-message');

    // Variables para almacenar datos
    let allUsers = [];
    let allEmails = [];

    // Inicializar
    initNavigation();
    loadDashboardData();
    loadUsers();
    loadEmails();

    // Funciones de Navegación
    function initNavigation() {
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const target = this.getAttribute('href').substring(1);
                
                // Actualizar enlace de navegación activo
                navLinks.forEach(nav => {
                    nav.classList.remove('bg-primary/20', 'text-primary');
                    nav.classList.add('text-text-secondary-dark', 'hover:bg-surface-dark', 'hover:text-text-primary-dark');
                });
                this.classList.remove('text-text-secondary-dark', 'hover:bg-surface-dark', 'hover:text-text-primary-dark');
                this.classList.add('bg-primary/20', 'text-primary');
                
                // Mostrar sección objetivo
                Object.values(sections).forEach(section => section.classList.add('hidden'));
                if (sections[target]) {
                    sections[target].classList.remove('hidden');
                }
                
                // Actualizar título de página
                updatePageTitle(target);
            });
        });

        // Mostrar panel principal por defecto
        sections.dashboard.classList.remove('hidden');
        updatePageTitle('dashboard');
        
        // Establecer enlace activo inicial
        navLinks[0].classList.add('bg-primary/20', 'text-primary');
        navLinks[0].classList.remove('text-text-secondary-dark', 'hover:bg-surface-dark', 'hover:text-text-primary-dark');
    }

    function updatePageTitle(section) {
        const titles = {
            dashboard: 'Panel Principal',
            users: 'Gestión de Usuarios',
            emails: 'Gestión de Correos'
        };
        pageTitle.textContent = titles[section] || 'CRM Dashboard';
    }

    // Funciones de Gestión de Usuarios
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
            showMessage('Todos los campos son obligatorios', 'error');
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
                return response.json().then(err => { throw new Error(err.error || 'Error de red'); });
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
                showMessage('Usuario agregado correctamente', 'success');
            }
        })
        .catch(error => {
            console.error('Error agregando usuario:', error);
            showMessage('Error agregando usuario: ' + error.message, 'error');
        });
    });

    function loadUsers() {
        console.log("Cargando usuarios...");
        fetch('/usuarios')
            .then(response => {
                if (!response.ok) {
                    throw new Error('La respuesta de la red no fue correcta');
                }
                return response.json();
            })
            .then(users => {
                console.log("Usuarios cargados:", users);
                allUsers = users; // Guardar todos los usuarios
                filterUsersTable(); // Aplicar filtros actuales
            })
            .catch(error => {
                console.error('Error cargando usuarios:', error);
                usersTableBody.innerHTML = `
                    <tr>
                        <td colspan="6" class="px-4 py-8 text-center text-red-400">
                            Error cargando usuarios: ${error.message}
                        </td>
                    </tr>
                `;
            });
    }

    // Funciones de filtrado para Usuarios
    function filterUsersTable() {
        const searchTerm = searchUsers.value.toLowerCase();
        const ageFilter = filterAge.value;
        const sortBy = filterSort.value;
        
        let filteredUsers = [...allUsers];
        
        // Aplicar búsqueda
        if (searchTerm) {
            filteredUsers = filteredUsers.filter(user => 
                user.nombre.toLowerCase().includes(searchTerm) || 
                user.apellido.toLowerCase().includes(searchTerm)
            );
        }
        
        // Aplicar filtro de edad
        if (ageFilter) {
            filteredUsers = filteredUsers.filter(user => {
                const age = user.edad;
                switch(ageFilter) {
                    case '18-25': return age >= 18 && age <= 25;
                    case '26-35': return age >= 26 && age <= 35;
                    case '36-50': return age >= 36 && age <= 50;
                    case '51+': return age >= 51;
                    default: return true;
                }
            });
        }
        
        // Aplicar ordenamiento
        filteredUsers.sort((a, b) => {
            switch(sortBy) {
                case 'newest':
                    return new Date(b.fecha_creacion) - new Date(a.fecha_creacion);
                case 'oldest':
                    return new Date(a.fecha_creacion) - new Date(b.fecha_creacion);
                case 'name_asc':
                    return (a.nombre + a.apellido).localeCompare(b.nombre + b.apellido);
                case 'name_desc':
                    return (b.nombre + b.apellido).localeCompare(a.nombre + a.apellido);
                case 'age_asc':
                    return a.edad - b.edad;
                case 'age_desc':
                    return b.edad - a.edad;
                default:
                    return 0;
            }
        });
        
        renderUsersTable(filteredUsers);
    }

    function renderUsersTable(users) {
        usersTableBody.innerHTML = '';
        
        if (users.length === 0) {
            usersTableBody.innerHTML = `
                <tr>
                    <td colspan="6" class="px-4 py-8 text-center text-text-secondary-dark">
                        No se encontraron usuarios que coincidan con los criterios
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
                        Eliminar
                    </button>
                </td>
            `;
            usersTableBody.appendChild(row);
        });
    }

    // Funciones de Gestión de Correos
    btnRefreshEmails.addEventListener('click', loadEmails);

    function loadEmails() {
        console.log("Cargando correos...");
        fetch('/correos')
            .then(response => {
                if (!response.ok) {
                    throw new Error('La respuesta de la red no fue correcta');
                }
                return response.json();
            })
            .then(emails => {
                console.log("Correos cargados:", emails);
                allEmails = emails; // Guardar todos los correos
                filterEmailsTable(); // Aplicar filtros actuales
            })
            .catch(error => {
                console.error('Error cargando correos:', error);
                emailsTableBody.innerHTML = `
                    <tr>
                        <td colspan="4" class="px-4 py-8 text-center text-red-400">
                            Error cargando correos: ${error.message}
                        </td>
                    </tr>
                `;
            });
    }

    // Funciones de filtrado para Correos
    function filterEmailsTable() {
        const searchTerm = searchEmails.value.toLowerCase();
        const providerFilter = filterProvider.value;
        const sortBy = filterSortEmails.value;
        
        let filteredEmails = [...allEmails];
        
        // Aplicar búsqueda
        if (searchTerm) {
            filteredEmails = filteredEmails.filter(email => 
                email.correo.toLowerCase().includes(searchTerm) ||
                email.nombre.toLowerCase().includes(searchTerm) ||
                email.apellido.toLowerCase().includes(searchTerm)
            );
        }
        
        // Aplicar filtro de proveedor
        if (providerFilter) {
            filteredEmails = filteredEmails.filter(email => email.tipo === providerFilter);
        }
        
        // Aplicar ordenamiento
        filteredEmails.sort((a, b) => {
            switch(sortBy) {
                case 'newest':
                    return new Date(b.fecha_creacion) - new Date(a.fecha_creacion);
                case 'oldest':
                    return new Date(a.fecha_creacion) - new Date(b.fecha_creacion);
                case 'provider':
                    return a.tipo.localeCompare(b.tipo);
                default:
                    return 0;
            }
        });
        
        renderEmailsTable(filteredEmails);
    }

    function renderEmailsTable(emails) {
        emailsTableBody.innerHTML = '';
        
        if (emails.length === 0) {
            emailsTableBody.innerHTML = `
                <tr>
                    <td colspan="4" class="px-4 py-8 text-center text-text-secondary-dark">
                        No se encontraron correos que coincidan con los criterios
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
    }

    // Funciones de Acción
    btnGenerateUsers.addEventListener('click', function() {
        const count = 100; // Cantidad por defecto para acción rápida
        generateRandomUsers(count);
    });

    btnMassGenerate.addEventListener('click', function() {
        const count = parseInt(massUsersCount.value) || 1000;
        if (count > 10000) {
            showMessage('El máximo permitido es 10,000 usuarios', 'error');
            return;
        }
        generateRandomUsers(count);
    });

    btnGenerateEmails.addEventListener('click', function() {
        generateEmailsConcurrent(); // Generar todos los tipos
    });

    // Nuevas funciones para selección de tipos de correo
    btnGenerateSelectedEmails.addEventListener('click', showEmailTypesModal);
    btnGenerateSelected.addEventListener('click', generateSelectedEmails);
    btnCancelSelection.addEventListener('click', hideEmailTypesModal);

    function showEmailTypesModal() {
        emailTypesModal.classList.remove('hidden');
    }

    function hideEmailTypesModal() {
        emailTypesModal.classList.add('hidden');
    }

    function generateSelectedEmails() {
        const selectedTypes = [];
        document.querySelectorAll('input[name="email-type"]:checked').forEach(checkbox => {
            selectedTypes.push(checkbox.value);
        });
        
        if (selectedTypes.length === 0) {
            showMessage('Por favor selecciona al menos un tipo de correo', 'error');
            return;
        }
        
        hideEmailTypesModal();
        generateEmailsConcurrent(selectedTypes);
    }

    function generateEmailsConcurrent(selectedTypes = null) {
        console.log("Generando correos con tipos:", selectedTypes);
        showProgress('Generando correos...', 0);
        
        let progress = 0;
        const interval = setInterval(() => {
            progress += 5;
            if (progress <= 90) {
                updateProgress('Generando correos...', progress);
            }
        }, 200);
        
        // Preparar datos para enviar
        const requestData = selectedTypes ? { tipos: selectedTypes } : {};
        
        fetch('/generar-correos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error || 'Error de red'); });
            }
            return response.json();
        })
        .then(data => {
            clearInterval(interval);
            console.log("Respuesta de generación de correos:", data);
            
            if (data.error) {
                throw new Error(data.error);
            }
            updateProgress('¡Completado!', 100);
            setTimeout(() => {
                hideProgress();
                loadEmails();
                loadDashboardData();
                const typeMessage = selectedTypes ? `Tipos seleccionados (${selectedTypes.length})` : 'Todos';
                showMessage(`Generados ${data.correos ? data.correos.length : 0} direcciones de correo (${typeMessage})`, 'success');
            }, 500);
        })
        .catch(error => {
            clearInterval(interval);
            console.error('Error generando correos:', error);
            hideProgress();
            showMessage('Error generando correos: ' + error.message, 'error');
        });
    }

    btnClearUsers.addEventListener('click', function() {
        if (confirm('¿Estás seguro de que quieres eliminar TODOS los usuarios? Esta acción no se puede deshacer.')) {
            fetch('/usuarios/todos', {
                method: 'DELETE'
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.error || 'Error de red'); });
                }
                return response.json();
            })
            .then(data => {
                loadUsers();
                loadEmails();
                loadDashboardData();
                showMessage('Todos los usuarios eliminados correctamente', 'success');
            })
            .catch(error => {
                console.error('Error eliminando usuarios:', error);
                showMessage('Error eliminando usuarios: ' + error.message, 'error');
            });
        }
    });

    btnClearEmails.addEventListener('click', function() {
        if (confirm('¿Estás seguro de que quieres eliminar TODOS los correos?')) {
            fetch('/correos/todos', {
                method: 'DELETE'
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.error || 'Error de red'); });
                }
                return response.json();
            })
            .then(data => {
                loadEmails();
                loadDashboardData();
                showMessage('Todos los correos eliminados correctamente', 'success');
            })
            .catch(error => {
                console.error('Error eliminando correos:', error);
                showMessage('Error eliminando correos: ' + error.message, 'error');
            });
        }
    });

    function generateRandomUsers(count) {
        console.log(`Generando ${count} usuarios aleatorios...`);
        showProgress('Generando usuarios aleatorios...', 0);
        
        fetch('/usuarios/aleatorios', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cantidad: count })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error || 'Error de red'); });
            }
            return response.json();
        })
        .then(data => {
            console.log("Respuesta de generación de usuarios:", data);
            if (data.error) {
                throw new Error(data.error);
            }
            updateProgress('¡Completado!', 100);
            setTimeout(() => {
                hideProgress();
                loadUsers();
                loadDashboardData();
                showMessage(`Generados ${data.usuarios ? data.usuarios.length : 0} usuarios aleatorios`, 'success');
            }, 500);
        })
        .catch(error => {
            console.error('Error generando usuarios:', error);
            hideProgress();
            showMessage('Error generando usuarios: ' + error.message, 'error');
        });
    }

    // Funciones del Panel Principal
    function loadDashboardData() {
        // Cargar conteo de usuarios
        fetch('/usuarios')
            .then(response => response.json())
            .then(users => {
                if (Array.isArray(users)) {
                    totalUsersCount.textContent = users.length;
                    usersGrowth.textContent = `+${users.length}`;
                }
            })
            .catch(error => {
                console.error('Error cargando conteo de usuarios:', error);
            });
        
        // Cargar conteo de correos
        fetch('/correos')
            .then(response => response.json())
            .then(emails => {
                if (Array.isArray(emails)) {
                    totalEmailsCount.textContent = emails.length;
                    emailsGrowth.textContent = `+${emails.length}`;
                    
                    // Contar proveedores únicos
                    const uniqueProviders = new Set(emails.map(email => email.tipo));
                    providersCount.textContent = `${uniqueProviders.size} Tipos`;
                }
            })
            .catch(error => {
                console.error('Error cargando conteo de correos:', error);
            });
    }

    // Funciones del Modal de Progreso
    function showProgress(title, percentage) {
        progressTitle.textContent = title;
        updateProgress('Iniciando...', percentage);
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

    // Funciones del Mensaje Toast
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

    // Event listeners para filtros
    searchUsers.addEventListener('input', filterUsersTable);
    filterAge.addEventListener('change', filterUsersTable);
    filterSort.addEventListener('change', filterUsersTable);
    searchEmails.addEventListener('input', filterEmailsTable);
    filterProvider.addEventListener('change', filterEmailsTable);
    filterSortEmails.addEventListener('change', filterEmailsTable);

    // Funciones globales
    window.deleteUser = function(id) {
        if (confirm('¿Estás seguro de que quieres eliminar este usuario?')) {
            fetch(`/usuarios/${id}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.error || 'Error de red'); });
                }
                return response.json();
            })
            .then(data => {
                loadUsers();
                loadEmails();
                loadDashboardData();
                showMessage('Usuario eliminado correctamente', 'success');
            })
            .catch(error => {
                console.error('Error eliminando usuario:', error);
                showMessage('Error eliminando usuario: ' + error.message, 'error');
            });
        }
    };
});
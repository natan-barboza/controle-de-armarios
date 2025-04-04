document.addEventListener("DOMContentLoaded", () => {
    var currentPath = window.location.pathname;

    const COLOR_TO_APPLY = 'bg-slate-800'

    if (currentPath === '/'){
        var element = document.getElementById("dashboard-li");
        element.classList.add(COLOR_TO_APPLY);
    } else if (currentPath === '/armarios/list/'){
        var element = document.getElementById("armarios-li");
        element.classList.add(COLOR_TO_APPLY);
    } else if (currentPath === '/solicitacoes/list/'){
        var element = document.getElementById("solicitacoes-li");
        element.classList.add(COLOR_TO_APPLY);
    } else if (currentPath === '/colaboradores/list/'){
        var element = document.getElementById("colaboradores-li");
        element.classList.add(COLOR_TO_APPLY);
    }

    
})
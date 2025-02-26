document.addEventListener('DOMContentLoaded', function() {
    fetchTeacherTrainingModules();
});

function fetchTeacherTrainingModules() {
    fetch('/teacher/training')
    .then(response => response.json())
    .then(modules => {
        const moduleList = document.getElementById('module-list');
        modules.forEach(module => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<a href="#" onclick="loadTrainingModule(${module.id})">${module.name}</a> - ${module.description}`;
            moduleList.appendChild(listItem);
        });
    });
}

function loadTrainingModule(moduleId) {
    fetch(`/teacher/training/${moduleId}`)
    .then(response => response.json())
    .then(module => {
        let content = `<h2>${module.name}</h2><p>${module.description}</p><p>${module.content}</p>`;
        if (module.video_url) {
            content += `<video width="320" height="240" controls><source src="${module.video_url}" type="video/mp4">Your browser does not support the video tag.</video>`;
        }
        if (module.pdf_url) {
            content += `<a href="${module.pdf_url}" target="_blank">View PDF Notes</a>`;
        }
        document.getElementById('content').innerHTML = content;
    });
}

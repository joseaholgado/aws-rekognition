//main.js
// Importar las funciones desde functions.js
import {
    triggerFileInput,
    showImagePreview,
    selectFile,
    transformImage
} from './functions.js';


// Seleccionar elementos HTML
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const uploadButton = document.getElementById('uploadButton');
const destFileList = document.getElementById('destFileList');
const preview = document.getElementById('preview');
const transformButton = document.getElementById('transformButton');
const fileList = document.getElementById('fileList');
let selectedFile = null;

// Cargar archivos del bucket destino y mostrarlos en la lista
fetch('/get-dest-files')
    .then(response => response.json())
    .then(data => {
        data.files.forEach(file => {
            const listItem = document.createElement('li');
            const fileLink = document.createElement('a');
            fileLink.href = `/download/${file}`;
            fileLink.textContent = file;
            listItem.appendChild(fileLink);
            destFileList.appendChild(listItem);
        });
    })
    .catch(error => console.error('Error al cargar los archivos del bucket destino:', error));

// Manejar clics en los botones de archivos en el bucket fuente
fileList.addEventListener('click', (e) => {
    if (e.target.tagName === 'BUTTON') {
        const fileName = e.target.textContent;
        selectFile(fileName);
    }
});

// Mostrar el botón de subir cuando un archivo se selecciona
fileInput.addEventListener('change', function() {
    if (this.files.length > 0) {
        uploadButton.style.display = 'inline';
        showImagePreview(this.files[0]);  // Llama a la función para mostrar la vista previa
    }
});

// Evento para hacer clic en dropZone y abrir el selector de archivos
dropZone.addEventListener('click', triggerFileInput);



// Manejo de arrastrar y soltar en dropZone
dropZone.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropZone.classList.add('dragover');  // Cambia el estilo al arrastrar un archivo
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');  // Elimina el estilo cuando se sale del área
});

dropZone.addEventListener('drop', (event) => {
    event.preventDefault();
    dropZone.classList.remove('dragover');

    // Obtener y asignar el archivo arrastrado al input
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        uploadButton.style.display = 'inline';
        showImagePreview(files[0]);  // Llama a la función para mostrar la vista previa
    }
});


// Función para manejar el envío de la imagen al servidor
uploadButton.addEventListener('click', function() {
    const file = fileInput.files[0];  // Obtener el archivo seleccionado

    if (!file) {
        alert('No se ha seleccionado ningún archivo.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);  // Agregar el archivo al FormData

    // Enviar el archivo al servidor
    fetch('/upload', {
        method: 'POST',
        body: formData  // El archivo se envía dentro del FormData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload(); 
    })
    .catch(error => {
        console.error('Error al subir la imagen:', error);
        alert('Error al subir la imagen.');
    });
});

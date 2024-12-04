// functions.js

// Exportar todas las funciones para que puedan ser usadas en otros archivos
function triggerFileInput() {
    fileInput.click();
}

// Función para mostrar la vista previa de la imagen seleccionada
function showImagePreview(file) {
    // Verificar que el archivo es una imagen
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        
        reader.onload = function(event) {
            preview.innerHTML = `<img src="${event.target.result}" alt="Vista previa de imagen" style="max-width:100%;">`;
        };
        
        reader.readAsDataURL(file);
    } else {
        preview.innerHTML = `<p>El archivo seleccionado no es una imagen.</p>`;
    }
}


// Función para seleccionar un archivo de la lista
function selectFile(fileName) {
    console.log("selectFile fue llamado para:", fileName);
    const fileExtension = fileName.split('.').pop().toLowerCase();

    if (['jpg', 'jpeg', 'png', 'gif', 'bmp'].includes(fileExtension)) {
        // Mostrar vista previa de imagen
        fetch(`/file-preview/${fileName}`)
            .then(response => {
                if (!response.ok) throw new Error("Error al obtener la vista previa del archivo");
                return response.blob();
            })
            .then(blob => {
                const objectURL = URL.createObjectURL(blob);
                preview.innerHTML = `<img src="${objectURL}" alt="Vista previa" style="max-width:100%;">`;
                transformButton.style.display = 'inline';
                transformButton.onclick = () => transformImage(fileName);
            })
            .catch(error => {
                console.error('Error al obtener la vista previa del archivo:', error);
                alert('Error al obtener la vista previa del archivo.');
            });
    } else if (fileExtension === 'json') {
        // Mostrar contenido JSON
        fetch(`/file-preview/${fileName}`)
            .then(response => response.json())
            .then(data => {
                preview.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                transformButton.style.display = 'none';
            })
            .catch(error => {
                console.error('Error al obtener el archivo JSON:', error);
                alert('Error al obtener el archivo JSON.');
            });
    } else if (fileExtension === 'mp3') {
        // Mostrar reproductor de audio
        preview.innerHTML = `<audio controls>
                                <source src="/file-preview/${fileName}" type="audio/mp3">
                                Tu navegador no soporta el reproductor de audio.
                             </audio>`;
        transformButton.style.display = 'none';
    } else {
        // Tipo de archivo no compatible
        preview.innerHTML = `<p>Este archivo no es compatible para vista previa.</p>`;
        transformButton.style.display = 'none';
    }
}


// Función para transformar la imagen
function transformImage(fileName) {
    fetch('/process-image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'file_name': fileName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
        } else {
            alert('Error al procesar la imagen.');
        }
    })
    .catch(error => {
        alert('Error al procesar la imagen.');
    });
}

export {triggerFileInput,
        showImagePreview,
        selectFile,
        transformImage};
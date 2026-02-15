/* =========================
   SELECTORES
========================= */
const lista = document.getElementById("lista-pdfs")
const btnAgregar = document.getElementById("agregar_archivo")
const inputArchivos = document.getElementById("inputArchivos")
const btnLimpiar = document.getElementById("limpiar")
const btnUnir = document.getElementById("unirPDFs")

let archivos = []

/* =========================
   FILE DIALOG
========================= */
btnAgregar.addEventListener("click", () => {
    inputArchivos.click()
})

inputArchivos.addEventListener("change", (e) => {
    const nuevos = Array.from(e.target.files)
    nuevos.forEach(file => archivos.push(file))
    console.log("📂 Archivos agregados:")
    console.table(archivos.map((f, i) => ({orden: i + 1, nombre: f.name})))
    renderizar()
})

/* =========================
   LIMPIAR
========================= */
btnLimpiar.addEventListener("click", () => {
    archivos = []
    console.log("🧹 Lista limpiada")
    renderizar()
})

/* =========================
   RENDER
========================= */
function renderizar() {
    lista.innerHTML = ""

    archivos.forEach((archivo, index) => {
        const card = document.createElement("div")
        card.classList.add("card-pdf")
        card.draggable = true
        card.dataset.index = index

        card.innerHTML = `
            <div class="numero-orden">${index + 1}</div>
            <button class="btn-eliminar">&times;</button>
            <div class="preview-pdf">PDF</div>
            <div class="mt-2">
                <small>${archivo.name}</small>
            </div>
        `

        // Botón eliminar visible al hover
        card.querySelector(".btn-eliminar").addEventListener("click", (e) => {
            e.stopPropagation()
            eliminarArchivo(card, index)
        })

        agregarEventosDrag(card)
        lista.appendChild(card)
    })
}

/* =========================
   ELIMINAR
========================= */
function eliminarArchivo(card, index) {
    console.log(`❌ Eliminando: ${archivos[index].name}`)
    card.classList.add("fade-out")
    setTimeout(() => {
        archivos.splice(index, 1)
        console.log("📋 Nuevo orden tras eliminar:")
        mostrarEstadoActual()
        renderizar()
    }, 250)
}

/* =========================
   DRAG & DROP
========================= */
let indiceInicial = null

function agregarEventosDrag(card) {
    card.addEventListener("dragstart", () => {
        card.classList.add("dragging")
        indiceInicial = parseInt(card.dataset.index)
        console.log(`🔄 Iniciando movimiento: posición ${indiceInicial + 1}`)
    })

    card.addEventListener("dragend", () => {
        card.classList.remove("dragging")
        actualizarOrdenInterno()
    })
}

lista.addEventListener("dragover", e => {
    e.preventDefault()
    const dragging = document.querySelector(".dragging")
    const afterElement = obtenerElementoDespuesDelMouse(e.clientY)
    if (afterElement == null) {
        lista.appendChild(dragging)
    } else {
        lista.insertBefore(dragging, afterElement)
    }
})

function obtenerElementoDespuesDelMouse(y) {
    const elementos = [...lista.querySelectorAll(".card-pdf:not(.dragging)")]
    return elementos.reduce((closest, child) => {
        const box = child.getBoundingClientRect()
        const offset = y - box.top - box.height / 2
        if (offset < 0 && offset > closest.offset) {
            return {offset: offset, element: child}
        } else {
            return closest
        }
    }, {offset: Number.NEGATIVE_INFINITY}).element
}

/* =========================
   SINCRONIZAR + LOGS
========================= */
function actualizarOrdenInterno() {
    const nuevasCards = [...lista.querySelectorAll(".card-pdf")]
    const nuevoOrden = []
    nuevasCards.forEach(card => {
        const indexOriginal = card.dataset.index
        nuevoOrden.push(archivos[indexOriginal])
    })
    archivos = nuevoOrden

    console.log("✅ Reorganización completada")
    console.log(`   Posición inicial: ${indiceInicial + 1}`)
    console.log("📋 Nuevo orden:")
    mostrarEstadoActual()
    renderizar()
}

function mostrarEstadoActual() {
    console.table(
        archivos.map((archivo, index) => ({
            orden: index + 1,
            nombre: archivo.name
        }))
    )
}

/* =========================
   SUBIR ARCHIVOS AL BACKEND
========================= */
async function subirArchivosAlBackend() {
    const rutasBackend = []

    for (const file of archivos) {
        const reader = new FileReader()
        await new Promise((resolve) => {
            reader.onload = async () => {
                const base64 = reader.result.split(",")[1]
                const rutaCompleta = await eel.subir_pdf(base64, file.name)()
                rutasBackend.push(rutaCompleta)
                resolve()
            }
            reader.readAsDataURL(file)
        })
    }

    console.log("📂 Rutas completas en backend:", rutasBackend)
    return rutasBackend
}

/* =========================
   UNIR PDFs
========================= */
btnUnir.addEventListener("click", async () => {
    if (archivos.length < 2) {
        alert("Selecciona al menos 2 PDFs")
        return
    }

    // 1️⃣ Subir archivos al backend y obtener rutas completas
    const listaRutas = await subirArchivosAlBackend()

    // 2️⃣ Pedir nombre del PDF final
    const nombreArchivo = prompt("Ingresa el nombre del PDF final:", "resultado.pdf")
    if (!nombreArchivo) return
    const rutaSalida = `data/output/${nombreArchivo}`

    // 3️⃣ Llamar a Python
    try {
        const resultado = await eel.unir(listaRutas, rutaSalida)()
        console.log(resultado)
        if (resultado.senal) {
            alert(`PDF generado correctamente: ${rutaSalida}`)
        } else {
            alert(`Error: ${resultado.mensaje}`)
        }
    } catch (error) {
        console.error("Error al unir PDFs:", error)
        alert(`Error inesperado al unir PDFs ${error}`)
    }
})

let daftartugas = [];

function renderTugas() {
    const list = document.getElementById("listtugas");
    const emptyMsg = document.getElementById("empty-message");
    const filter = document.getElementById("filter").value;
    list.innerHTML = "";

    // Filter tugas
    let filtered = daftartugas;
    if (filter !== "Semua") {
        filtered = daftartugas.filter(t => t.status === filter);
    }

    if (filtered.length === 0) {
        emptyMsg.style.display = "block";
    } else {
        emptyMsg.style.display = "none";
    }

    filtered.forEach((tugas, idx) => {
        const li = document.createElement("li");
        li.className = tugas.status === "Selesai" ? "completed" : "";
        li.textContent = `${tugas.task} (${tugas.date})`;

        // Tombol selesai
        const doneBtn = document.createElement("button");
        doneBtn.textContent = tugas.status === "Selesai" ? "Batal" : "Selesai";
        doneBtn.className = "status-btn done";
        doneBtn.onclick = function() {
            daftartugas[idx].status = tugas.status === "Selesai" ? "Belum Selesai" : "Selesai";
            renderTugas();
        };

        // Tombol hapus
        const delBtn = document.createElement("button");
        delBtn.textContent = "Hapus";
        delBtn.className = "status-btn delete";
        delBtn.onclick = function() {
            daftartugas.splice(idx, 1);
            renderTugas();
        };

        li.appendChild(doneBtn);
        li.appendChild(delBtn);
        list.appendChild(li);
    });
}

function tambahtugas(event) {
    event.preventDefault();
    const inputtask = document.getElementById("inputtugas");
    const inputdate = document.getElementById("inputtanggal");
    if (inputtask.value === "" || inputdate.value === "") {
        alert("Mohon Isi Tugas dan Tanggal !");
        return;
    }
    daftartugas.push({
        task: inputtask.value,
        date: inputdate.value,
        status: "Belum Selesai"
    });
    inputtask.value = "";
    inputdate.value = "";
    renderTugas();
}

function hapustugas() {
    daftartugas = [];
    renderTugas();
}

document.getElementById("form-tugas").addEventListener("submit", tambahtugas);
document.getElementById("delete-all").addEventListener("click", hapustugas);
document.getElementById("filter").addEventListener("change", renderTugas);

document.addEventListener("DOMContentLoaded", renderTugas);
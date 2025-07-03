const apiUrl = "http://localhost:5000/catalogues";
let allCatalogues = [];
let currentPage = 1;
const rowsPerPage = 5;
let isEditMode = false;
let editCatalogueId = null;

function initCatalogueView() {
  getAllCatalogues();
  showSection("all_catalogues");
}

function showSection(id) {
  document.querySelectorAll(".section").forEach((s) => (s.style.display = "none"));
  document.getElementById(id).style.display = "flex";

  if (id === "create") {
    resetForm();
  }

  if (id === "all_catalogues") getAllCatalogues();
}

function formatDate(dateStr) {
  const date = new Date(dateStr);
  const day = String(date.getDate()).padStart(2, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const year = date.getFullYear();
  return `${year}-${month}-${day}`;
}

function resetForm() {
  document.getElementById("c_name").value = "";
  document.getElementById("c_desc").value = "";
  document.getElementById("c_from").value = "";
  document.getElementById("c_to").value = "";
  document.getElementById("c_status").value = "";
  isEditMode = false;
  editCatalogueId = null;

  const saveBtn = document.querySelector("#create button");
  saveBtn.textContent = "💾 Save";
  saveBtn.onclick = createCatalogue;
}

function createCatalogue() {
  const data = {
    catalogue_name: document.getElementById("c_name").value,
    catalogue_description: document.getElementById("c_desc").value,
    effective_from: document.getElementById("c_from").value,
    effective_to: document.getElementById("c_to").value,
    status: document.getElementById("c_status").value,
  };

  fetch(apiUrl, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then((res) => {
    if (res.ok) {
      alert("✅ Catalogue Created");
      initCatalogueView();
    } else {
      alert("❌ Failed to create catalogue");
    }
  });
}

function updateCatalogue() {
  const data = {
    catalogue_name: document.getElementById("c_name").value,
    catalogue_description: document.getElementById("c_desc").value,
    effective_from: document.getElementById("c_from").value,
    effective_to: document.getElementById("c_to").value,
    status: document.getElementById("c_status").value,
  };

  fetch(`${apiUrl}/${editCatalogueId}`, {
    method: "PUT",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then((res) => {
    if (res.ok) {
      alert("✏️ Catalogue Updated");
      initCatalogueView();
      showSection("all_catalogues");
    } else {
      alert("❌ Failed to update catalogue");
    }
  });
}

function getAllCatalogues() {
  fetch(apiUrl, {
    method: "GET",
    credentials: "include"
  })
    .then((res) => {
      if (!res.ok) throw new Error("Unauthorized or failed to fetch");
      return res.json();
    })
    .then((data) => {
      allCatalogues = data.reverse(); // Show newest first
      currentPage = 1;
      renderTable();
    })
    .catch((err) => {
      alert("⚠️ Error: " + err.message);
    });
}

function searchById() {
  const id = document.getElementById("get_id").value;
  if (!id) {
    alert("❗Please enter a valid ID");
    return;
  }

  fetch(`${apiUrl}/${id}`, { credentials: "include" })
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        alert("❌ Catalogue not found!");
        return;
      }

      allCatalogues = [data];
      currentPage = 1;
      renderTable();
    })
    .catch(() => {
      alert("❌ Error fetching catalogue by ID");
    });
}

function filterCataloguesByStatus(status) {
  const filtered = allCatalogues.filter((c) => c.status === status);
  currentPage = 1;
  renderTable(filtered);
}

function renderTable(data = allCatalogues) {
  const tbody = document.getElementById("all_data");
  tbody.innerHTML = "";

  const start = (currentPage - 1) * rowsPerPage;
  const end = start + rowsPerPage;
  const pageItems = data.slice(start, end);

  pageItems.forEach((c) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${c.catalogue_id}</td>
      <td>${c.catalogue_name}</td>
      <td>${c.catalogue_description}</td>
      <td>${formatDate(c.effective_from)}</td>
      <td>${formatDate(c.effective_to)}</td>
      <td><span class="status ${c.status.toLowerCase()}">${c.status}</span></td>
      <td>
        <button class="action-btn" onclick="editCatalogue(${c.catalogue_id})">✏️</button>
        <button class="emoji-btn" title="Delete" onclick="deleteById(${c.catalogue_id})">🗑️</button>
      </td>
    `;
    tbody.appendChild(row);
  });

  document.getElementById("page_info").textContent =
    `Page ${currentPage} of ${Math.ceil(data.length / rowsPerPage)}`;
}

function editCatalogue(id) {
  const catalogue = allCatalogues.find((c) => c.catalogue_id === id);
  if (!catalogue) return alert("❌ Catalogue not found");

  showSection("create");

  document.getElementById("c_name").value = catalogue.catalogue_name;
  document.getElementById("c_desc").value = catalogue.catalogue_description;
  document.getElementById("c_from").value = formatDate(catalogue.effective_from);
  document.getElementById("c_to").value = formatDate(catalogue.effective_to);
  document.getElementById("c_status").value = catalogue.status;

  isEditMode = true;
  editCatalogueId = id;

  const saveBtn = document.querySelector("#create button");
  saveBtn.textContent = "✏️ Update";
  saveBtn.onclick = updateCatalogue;
}

function nextPage() {
  if (currentPage < Math.ceil(allCatalogues.length / rowsPerPage)) {
    currentPage++;
    renderTable();
  }
}

function prevPage() {
  if (currentPage > 1) {
    currentPage--;
    renderTable();
  }
}

function deleteById(id) {
  if (confirm("Are you sure you want to delete this catalogue?")) {
    fetch(`${apiUrl}/${id}`, {
      method: "DELETE",
      credentials: "include"
    }).then(() => {
      alert("🗑️ Catalogue Deleted");
      initCatalogueView();
    });
  }
}

function exitApp() {
  location.reload();
}


function logout() {
  fetch("http://localhost:5000/logout", {
    method: "POST",
    credentials: "include"
  })
    .then((res) => res.json())
    .then((data) => {
      alert(data.message || "Logged out");
      window.location.href = "/login.html"; // redirect to login
    })
    .catch(() => {
      alert("❌ Failed to log out");
    });
}

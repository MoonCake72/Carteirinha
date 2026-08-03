// ------------------- NAVEGAÇÃO & ROTAÇÃO 3D DO CARTÃO -------------------
function setupCardNavigation() {
  const card = document.getElementById("card");
  const navButtons = document.querySelectorAll(".nav-btn");

  if (!card) return;

  // Atualiza a classe 'active' das abas superiores baseando-se na face atual
  const updateNavButtons = (face) => {
    navButtons.forEach((btn) => {
      const targetPage = btn.getAttribute("data-page");
      // Mapeia 'front' e 'back' para o botão de Carteirinha
      if ((targetPage === "front" && (face === "front" || face === "back")) || targetPage === face) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });
  };

  // 1. Clique no cartão para ciclar entre FRENTE -> VERSO -> VACINAS -> FRENTE
  card.addEventListener("click", (e) => {
    // Evita disparar a rotação ao clicar em elementos interativos
    const isInteractive = e.target.closest('[contenteditable="true"]') ||
                          e.target.closest('.editable-field') ||
                          e.target.closest('input') ||
                          e.target.closest('select') ||
                          e.target.closest('button') ||
                          e.target.closest('.history-list');

    if (isInteractive) return;

    const currentFace = card.getAttribute("data-face") || "front";
    let nextFace = "front";

    if (currentFace === "front") {
      nextFace = "back";
    } else if (currentFace === "back") {
      nextFace = "vaccines";
    } else {
      nextFace = "front";
    }

    card.setAttribute("data-face", nextFace);
    updateNavButtons(nextFace);
  });

  // 2. Clique nas abas superiores para ir direto para uma face
  navButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const targetPage = btn.getAttribute("data-page");
      card.setAttribute("data-face", targetPage);
      updateNavButtons(targetPage);
    });
  });
}

// ------------------- LÓGICA DE VACINAS (LOCALSTORAGE) -------------------
function setupVaccinesSystem() {
  const form = document.getElementById("vaccine-form");
  if (!form) return;

  const petNameInput = document.getElementById("pet-name");
  const dateInput = document.getElementById("vaccine-date");
  const vaccineTypeSelect = document.getElementById("vaccine-type");
  const historyList = document.getElementById("history-list");
  const emptyMsg = document.getElementById("empty-msg");
  const clearHistoryBtn = document.getElementById("clear-history-btn");

  let vaccines = JSON.parse(localStorage.getItem("cat_vaccines")) || [];

  function formatDate(dateStr) {
    if (!dateStr) return "";
    const [year, month, day] = dateStr.split("-");
    return `${day}/${month}/${year}`;
  }

  function renderHistory() {
    if (!historyList) return;
    historyList.innerHTML = "";

    if (vaccines.length === 0) {
      if (emptyMsg) {
        historyList.appendChild(emptyMsg);
        emptyMsg.style.display = "block";
      }
      return;
    }

    if (emptyMsg) emptyMsg.style.display = "none";

    vaccines.forEach((v, index) => {
      const item = document.createElement("div");
      item.className = "vaccine-item";
      item.innerHTML = `
        <div>
          <strong>${v.type} (${v.name})</strong>
          <span>Aplicada em: ${formatDate(v.date)}</span>
        </div>
        <button type="button" class="btn-delete-item" onclick="removeVaccine(${index})">✕</button>
      `;
      historyList.appendChild(item);
    });
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const newVaccine = {
      name: petNameInput.value.trim(),
      date: dateInput.value,
      type: vaccineTypeSelect.value,
    };

    vaccines.unshift(newVaccine);
    localStorage.setItem("cat_vaccines", JSON.stringify(vaccines));

    petNameInput.value = "";
    dateInput.value = "";
    renderHistory();
  });

  window.removeVaccine = function (index) {
    vaccines.splice(index, 1);
    localStorage.setItem("cat_vaccines", JSON.stringify(vaccines));
    renderHistory();
  };

  if (clearHistoryBtn) {
    clearHistoryBtn.addEventListener("click", () => {
      if (confirm("Deseja apagar todo o histórico de vacinas?")) {
        vaccines = [];
        localStorage.removeItem("cat_vaccines");
        renderHistory();
      }
    });
  }

  renderHistory();
}

// ------------------- CARREGAMENTO DE DADOS DA API -------------------
async function loadCardData(cardId = "0007-GATA") {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/card/${cardId}`);
    if (!response.ok) throw new Error("Erro ao carregar dados do banco");

    const data = await response.json();

    // Preenche a FRENTE
    const nameEl = document.querySelector(".cat-name");
    if (nameEl) nameEl.textContent = data.name;

    const titleEl = document.querySelector(".cat-title");
    if (titleEl) titleEl.textContent = data.title;

    const idEl = document.querySelector(".id-num");
    if (idEl) idEl.textContent = `ID Nº ${data.id_number}`;

    // Helper para preencher os campos editáveis do verso pelo atributo data-field
    const setFieldValue = (field, val) => {
      const el = document.querySelector(`.editable-field[data-field="${field}"]`);
      if (el) el.textContent = val !== undefined && val !== null && val !== "" ? val : (field === "second_owner" ? "Opcional" : "");
    };

    setFieldValue("breed", data.breed);
    setFieldValue("birth_date", data.birth_date);
    setFieldValue("color", data.color);
    setFieldValue("owner", data.owner);
    setFieldValue("second_owner", data.second_owner);
    setFieldValue("superpower", data.superpower);
    setFieldValue("favorite_food", data.favorite_food);

  } catch (error) {
    console.error("Erro na integração:", error);
  }
}

// ------------------- EDICAO DOS CAMPOS (API PATCH) -------------------
async function saveCatName(cardId, newName) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/card/${cardId}/name`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newName }),
    });
    if (!response.ok) throw new Error("Erro ao salvar o nome no banco");
  } catch (error) {
    console.error("Erro ao atualizar o nome:", error);
  }
}

function setupNameEditing(cardId = "0007-GATA") {
  const nameEl = document.querySelector(".cat-name");
  if (!nameEl) return;

  nameEl.addEventListener("click", (e) => e.stopPropagation());
  nameEl.addEventListener("blur", () => {
    const updatedName = nameEl.textContent.trim();
    if (updatedName !== "") saveCatName(cardId, updatedName);
  });
  nameEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      nameEl.blur();
    }
  });
}

async function saveCatTitle(cardId, newTitle) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/card/${cardId}/title`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newTitle }),
    });
    if (!response.ok) throw new Error("Erro ao salvar o cargo no banco");
  } catch (error) {
    console.error("Erro ao atualizar o cargo:", error);
  }
}

function setupTitleEditing(cardId = "0007-GATA") {
  const titleEl = document.querySelector(".cat-title");
  if (!titleEl) return;

  titleEl.addEventListener("click", (e) => e.stopPropagation());
  titleEl.addEventListener("blur", () => {
    const updatedTitle = titleEl.textContent.trim();
    if (updatedTitle !== "") saveCatTitle(cardId, updatedTitle);
  });
  titleEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      titleEl.blur();
    }
  });
}

async function saveCatBreed(cardId, newBreed) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/card/${cardId}/breed`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ breed: newBreed }),
    });
    if (!response.ok) throw new Error("Erro ao salvar a raça no banco");
  } catch (error) {
    console.error("Erro ao atualizar a raça:", error);
  }
}

function setupBreedEditing(cardId = "0007-GATA") {
  const breedEl = document.querySelector('.editable-field[data-field="breed"]');
  if (!breedEl) return;

  breedEl.addEventListener("click", (e) => e.stopPropagation());
  breedEl.addEventListener("blur", () => {
    const updatedBreed = breedEl.textContent.trim();
    if (updatedBreed !== "") saveCatBreed(cardId, updatedBreed);
  });
  breedEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      breedEl.blur();
    }
  });
}

async function saveCatBirthDate(cardId, newBirthDate) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/card/${cardId}/birth_date`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ birth_date: newBirthDate }),
    });
    if (!response.ok) throw new Error("Erro ao salvar a data de nascimento no banco");
  } catch (error) {
    console.error("Erro ao atualizar a data de nascimento:", error);
  }
}

function setupBirthDateEditing(cardId = "0007-GATA") {
  const birthEl = document.querySelector('.editable-field[data-field="birth_date"]');
  if (!birthEl) return;

  birthEl.addEventListener("click", (e) => e.stopPropagation());
  birthEl.addEventListener("blur", () => {
    const updatedBirthDate = birthEl.textContent.trim();
    if (updatedBirthDate !== "") saveCatBirthDate(cardId, updatedBirthDate);
  });
  birthEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      birthEl.blur();
    }
  });
}

async function saveCatColor(cardId, newColor) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/card/${cardId}/color`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ color: newColor }),
    });
    if (!response.ok) throw new Error("Erro ao salvar a cor no banco");
  } catch (error) {
    console.error("Erro ao atualizar a cor:", error);
  }
}

function setupColorEditing(cardId = "0007-GATA") {
  const colorEl = document.querySelector('.editable-field[data-field="color"]');
  if (!colorEl) return;

  colorEl.addEventListener("click", (e) => e.stopPropagation());
  colorEl.addEventListener("blur", () => {
    const updatedColor = colorEl.textContent.trim();
    if (updatedColor !== "") saveCatColor(cardId, updatedColor);
  });
  colorEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      colorEl.blur();
    }
  });
}

async function saveCatOwner(cardId, newOwner) {
  try {
    await fetch(`http://127.0.0.1:8000/api/card/${cardId}/owner`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ owner: newOwner }),
    });
  } catch (error) {
    console.error("Erro ao atualizar Tutor 1:", error);
  }
}

async function saveCatSecondOwner(cardId, newSecondOwner) {
  try {
    await fetch(`http://127.0.0.1:8000/api/card/${cardId}/second_owner`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ second_owner: newSecondOwner }),
    });
  } catch (error) {
    console.error("Erro ao atualizar Tutor 2:", error);
  }
}

function setupOwnersEditing(cardId = "0007-GATA") {
  const owner1El = document.querySelector('.editable-field[data-field="owner"]');
  const owner2El = document.querySelector('.editable-field[data-field="second_owner"]');

  if (owner1El) {
    owner1El.addEventListener("click", (e) => e.stopPropagation());
    owner1El.addEventListener("blur", () => saveCatOwner(cardId, owner1El.textContent.trim()));
    owner1El.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        owner1El.blur();
      }
    });
  }

  if (owner2El) {
    owner2El.addEventListener("click", (e) => e.stopPropagation());
    owner2El.addEventListener("blur", () => saveCatSecondOwner(cardId, owner2El.textContent.trim()));
    owner2El.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        owner2El.blur();
      }
    });
  }
}

async function saveCatSuperpower(cardId, newSuperpower) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/card/${cardId}/superpower`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ superpower: newSuperpower }),
    });
    if (!response.ok) throw new Error("Erro ao salvar o superpoder no banco");
  } catch (error) {
    console.error("Erro ao atualizar o superpoder:", error);
  }
}

function setupSuperpowerEditing(cardId = "0007-GATA") {
  const superpowerEl = document.querySelector('.editable-field[data-field="superpower"]');
  if (!superpowerEl) return;

  superpowerEl.addEventListener("click", (e) => e.stopPropagation());
  superpowerEl.addEventListener("blur", () => {
    const updatedSuperpower = superpowerEl.textContent.trim();
    if (updatedSuperpower !== "") saveCatSuperpower(cardId, updatedSuperpower);
  });
  superpowerEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      superpowerEl.blur();
    }
  });
}

async function saveCatFavoriteFood(cardId, newFood) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/card/${cardId}/favorite_food`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ favorite_food: newFood }),
    });
    if (!response.ok) throw new Error("Erro ao salvar a comida favorita no banco");
  } catch (error) {
    console.error("Erro ao atualizar a comida favorita:", error);
  }
}

function setupFavoriteFoodEditing(cardId = "0007-GATA") {
  const foodEl = document.querySelector('.editable-field[data-field="favorite_food"]');
  if (!foodEl) return;

  foodEl.addEventListener("click", (e) => e.stopPropagation());
  foodEl.addEventListener("blur", () => {
    const updatedFood = foodEl.textContent.trim();
    if (updatedFood !== "") saveCatFavoriteFood(cardId, updatedFood);
  });
  foodEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      foodEl.blur();
    }
  });
}

// ------------------- INICIALIZAÇÃO DA PÁGINA -------------------
document.addEventListener("DOMContentLoaded", () => {
  setupCardNavigation();
  setupVaccinesSystem();
  
  loadCardData("0007-GATA");
  setupNameEditing("0007-GATA");
  setupTitleEditing("0007-GATA");
  setupBreedEditing("0007-GATA");
  setupBirthDateEditing("0007-GATA");
  setupColorEditing("0007-GATA");
  setupOwnersEditing("0007-GATA");
  setupSuperpowerEditing("0007-GATA");
  setupFavoriteFoodEditing("0007-GATA");
});
const card = document.getElementById("card");

// Vira a carteirinha ao clicar no cartão
card.addEventListener("click", () => {
  card.classList.toggle("flipped");
});

// Carrega os dados da API ao abrir a página
async function loadCardData(cardId = "0007-GATA") {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/card/${cardId}`);
    if (!response.ok) throw new Error("Erro ao carregar dados do banco");

    const data = await response.json();

    // Preenche a FRENTE
    const nameEl = document.querySelector(".cat-name");
    if (nameEl) nameEl.textContent = data.name;

    document.querySelector(".cat-title").textContent = data.title;
    document.querySelector(".id-num").textContent = `ID Nº ${data.id_number}`;

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

// ------------------- FRENTE: NOME -------------------
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

// ------------------- FRENTE: CARGO -------------------
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

// ------------------- VERSO: RAÇA -------------------
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

// ------------------- VERSO: NASCIMENTO -------------------
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

// ------------------- VERSO: COR -------------------
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

// ------------------- VERSO: TUTOR 1 & TUTOR 2 -------------------
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

// Salva o novo superpoder no banco via API
async function saveCatSuperpower(cardId, newSuperpower) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/card/${cardId}/superpower`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ superpower: newSuperpower }),
    });
    if (!response.ok) throw new Error("Erro ao salvar o superpoder no banco");
    console.log("Superpoder atualizado com sucesso no PostgreSQL!");
  } catch (error) {
    console.error("Erro ao atualizar o superpoder:", error);
  }
}

// Configura a edição do campo de superpoder
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

// INICIALIZAÇÃO DA PÁGINA
document.addEventListener("DOMContentLoaded", () => {
  loadCardData("0007-GATA");
  setupNameEditing("0007-GATA");
  setupTitleEditing("0007-GATA");
  setupBreedEditing("0007-GATA");
  setupBirthDateEditing("0007-GATA");
  setupColorEditing("0007-GATA");
  setupOwnersEditing("0007-GATA");
  setupSuperpowerEditing("0007-GATA");
});
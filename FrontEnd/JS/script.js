const card = document.getElementById("card");

// Vira a carteirinha ao clicar no cartão
card.addEventListener("click", () => {
  card.classList.toggle("flipped");
});

// Carrega os dados da API ao abrir a página
async function loadCardData(cardId = 1) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/card/${cardId}`);
    if (!response.ok) throw new Error("Erro ao carregar dados do banco");

    const data = await response.json();

    // Preenche a FRENTE
    const nameEl = document.querySelector(".cat-name");
    if (nameEl) nameEl.textContent = data.name;

    document.querySelector(".cat-title").textContent = data.title;
    document.querySelector(".id-num").textContent = `ID Nº ${data.id_number}`;

    // Preenche o VERSO
    const fields = document.querySelectorAll(".field");
    if (fields.length >= 6) {
      fields[0].querySelectorAll("span")[1].textContent = data.breed;
      fields[1].querySelectorAll("span")[1].textContent = data.birth_date;
      fields[2].querySelectorAll("span")[1].textContent = data.color;
      fields[3].querySelectorAll("span")[1].textContent = data.owner;
      fields[4].querySelectorAll("span")[1].textContent = data.superpower;
      fields[5].querySelectorAll("span")[1].textContent = data.favorite_food;
    }
  } catch (error) {
    console.error("Erro na integração:", error);
  }
}

// Salva o novo nome no banco de dados via API
async function saveCatName(cardId, newName) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/card/${cardId}/name`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: newName }),
    });

    if (!response.ok) throw new Error("Erro ao salvar o nome no banco");
    console.log("Nome atualizado com sucesso no PostgreSQL!");
  } catch (error) {
    console.error("Erro ao atualizar o nome:", error);
  }
}

// Configura a edição do campo de nome
function setupNameEditing(cardId = 1) {
  const nameEl = document.querySelector(".cat-name");
  if (!nameEl) return;

  // Evita que o clique no nome dispare o evento de virar o cartão
  nameEl.addEventListener("click", (e) => {
    e.stopPropagation();
  });

  // Salva alterações ao sair do campo (perder o foco)
  nameEl.addEventListener("blur", () => {
    const updatedName = nameEl.textContent.trim();
    if (updatedName !== "") {
      saveCatName(cardId, updatedName);
    }
  });

  // Salva alterações ao pressionar Enter e remove o foco
  nameEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault(); // Evita quebra de linha no nome
      nameEl.blur(); // Dispara o evento 'blur'
    }
  });
}

// Inicializa quando a página carrega
document.addEventListener("DOMContentLoaded", () => {
  loadCardData(1);
  setupNameEditing(1);
});
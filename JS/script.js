//Seleciona a carteirinha
const card = document.getElementById("card");

//Vira a carteirinha ao clicar
card.addEventListener("click", () => {
    card.classList.toggle("flipped");
});
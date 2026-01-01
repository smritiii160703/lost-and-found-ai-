const API = "http://localhost:8000";

document.getElementById("reportForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(e.target);

  const res = await fetch(`${API}/report`, {
    method: "POST",
    body: formData,
  });

  const data = await res.json();

  let html = `<h3>Possible Matches</h3>`;

  data.matches.forEach(m => {
    html += `
      <div>
        <b>${m.title}</b> (${m.type})<br>
        ${m.description}<br>
        ${m.image ? `<img src="${API}/${m.image}" width="120">` : ""}
      </div><hr>`;
  });

  document.getElementById("results").innerHTML = html;
});


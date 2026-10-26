const $ = (id) => document.getElementById(id);
let mode = "encrypt";

document.querySelectorAll(".tab").forEach((btn) =>
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    mode = btn.dataset.mode;
    $("go").textContent = mode === "encrypt" ? "Encrypt file" : "Decrypt file";
    setStatus("");
  })
);

$("file").addEventListener("change", () => {
  $("fileName").textContent = $("file").files[0]?.name || "Click or drop a file here";
});

const drop = $("drop");
drop.addEventListener("dragover", (e) => { e.preventDefault(); drop.classList.add("over"); });
drop.addEventListener("dragleave", () => drop.classList.remove("over"));
drop.addEventListener("drop", (e) => {
  e.preventDefault(); drop.classList.remove("over");
  $("file").files = e.dataTransfer.files;
  $("file").dispatchEvent(new Event("change"));
});

function setStatus(msg, type = "") {
  $("status").textContent = msg;
  $("status").className = "status " + type;
}

$("go").addEventListener("click", async () => {
  const file = $("file").files[0];
  const password = $("password").value;
  if (!file) return setStatus("Please choose a file.", "err");
  if (!password) return setStatus("Please enter a password.", "err");

  const form = new FormData();
  form.append("file", file);
  form.append("password", password);

  $("go").disabled = true;
  setStatus("Working…");
  try {
    const res = await fetch(`/api/${mode}`, { method: "POST", body: form });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Something went wrong.");
    }
    const blob = await res.blob();
    const name = /filename="(.+)"/.exec(res.headers.get("Content-Disposition"))?.[1] || "output";
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = name;
    a.click();
    URL.revokeObjectURL(a.href);
    setStatus(`Done! Saved as ${name}`, "ok");
  } catch (e) {
    setStatus(e.message, "err");
  } finally {
    $("go").disabled = false;
  }
});

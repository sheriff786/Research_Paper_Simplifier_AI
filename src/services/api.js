const BASE_URL = "http://localhost:8000/api/v1";

export async function uploadPaper(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/papers/upload`, {
    method: "POST",
    body: formData
  });
  return res.json();
}

export async function chatWithPaper(paperId, message) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ paper_id: paperId, message })
  });
  return res.json();
}

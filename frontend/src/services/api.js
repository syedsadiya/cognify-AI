async function request(path, options) {
  const res = await fetch("/api" + path, options);
  if (!res.ok) {
    let message = "Request failed";
    try {
      const data = await res.json();
      message = data.detail || message;
    } catch (e) {}
    throw new Error(message);
  }
  if (res.status === 204) return null;
  return res.json();
}

export function getHealth() {
  return request("/health");
}

export function getDashboardSummary() {
  return request("/dashboard/summary");
}

export function getSettings() {
  return request("/settings");
}

export function sendAssistantChat(message, history, datasetId) {
  return request("/assistant/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history, dataset_id: datasetId || null }),
  });
}

export function saveSetting(key, value) {
  return request("/settings", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ key, value }),
  });
}

export function listDatasets() {
  return request("/datasets");
}

export function getPreview(id, rows = 20) {
  return request("/datasets/" + id + "/preview?rows=" + rows);
}

export function getProfile(id) {
  return request("/datasets/" + id + "/profile");
}

export function deleteDataset(id) {
  return request("/datasets/" + id, { method: "DELETE" });
}

export function downloadUrl(id) {
  return "/api/datasets/" + id + "/download";
}

// Uses XMLHttpRequest because fetch cannot report upload progress.
export function uploadDataset(file, onProgress) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/datasets/upload");

    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable) onProgress(Math.round((e.loaded / e.total) * 100));
    };

    xhr.onload = () => {
      let data = {};
      try {
        data = JSON.parse(xhr.responseText);
      } catch (e) {}
      if (xhr.status >= 200 && xhr.status < 300) resolve(data);
      else reject(new Error(data.detail || "Upload failed"));
    };

    xhr.onerror = () => reject(new Error("Could not reach the server"));

    const form = new FormData();
    form.append("file", file);
    xhr.send(form);
  });
}

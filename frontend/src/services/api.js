const API_BASE = '/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Health check failed');
  return res.json();
}

export async function fetchExams(stream = 'PCM') {
  const res = await fetch(`${API_BASE}/exams?stream=${encodeURIComponent(stream)}`);
  if (!res.ok) throw new Error('Failed to fetch examinations');
  return res.json();
}

export async function fetchExamMeta(examCode, year = 2024) {
  const res = await fetch(`${API_BASE}/exams/${examCode}/meta?year=${year}`);
  if (!res.ok) throw new Error(`Failed to fetch metadata for ${examCode}`);
  return res.json();
}

export async function searchCutoffs(params) {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') {
      searchParams.append(k, v);
    }
  });
  const res = await fetch(`${API_BASE}/cutoffs/search?${searchParams.toString()}`);
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || 'Failed to search cutoffs');
  }
  return res.json();
}

export async function fetchColleges(params = {}) {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') {
      searchParams.append(k, v);
    }
  });
  const res = await fetch(`${API_BASE}/colleges?${searchParams.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch colleges');
  return res.json();
}

export async function fetchCollegeDetails(collegeId) {
  const res = await fetch(`${API_BASE}/colleges/${collegeId}`);
  if (!res.ok) throw new Error(`Failed to fetch college details for ${collegeId}`);
  return res.json();
}

export async function fetchCutoffTrends(collegeId, branchId, category = 'OPEN', quota = 'AI') {
  const res = await fetch(`${API_BASE}/colleges/${collegeId}/trends?branch_id=${branchId}&category=${encodeURIComponent(category)}&quota=${encodeURIComponent(quota)}`);
  if (!res.ok) throw new Error('Failed to fetch cutoff trends');
  return res.json();
}

export async function fetchBranches(params = {}) {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v) searchParams.append(k, v);
  });
  const res = await fetch(`${API_BASE}/branches?${searchParams.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch branches');
  return res.json();
}

export async function fetchCareerPaths() {
  const res = await fetch(`${API_BASE}/career/paths`);
  if (!res.ok) throw new Error('Failed to fetch career pathways');
  return res.json();
}

export async function generatePersonalizedRoadmap(payload) {
  const res = await fetch(`${API_BASE}/career/roadmap/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error('Failed to generate roadmap');
  return res.json();
}

export async function fetchDataQualityReports(year = 2024) {
  const res = await fetch(`${API_BASE}/admin/data-quality?year=${year}`);
  if (!res.ok) throw new Error('Failed to fetch data quality reports');
  return res.json();
}

export async function fetchSyncStatus() {
  const res = await fetch(`${API_BASE}/admin/sync-status`);
  if (!res.ok) throw new Error('Failed to fetch sync status');
  return res.json();
}

export async function triggerManualSync(examCode, year = 2024) {
  const res = await fetch(`${API_BASE}/admin/sync/${examCode}?year=${year}`, {
    method: 'POST'
  });
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || 'Failed to trigger sync');
  }
  return res.json();
}

export async function searchNeetCutoffs(params) {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') {
      searchParams.append(k, v);
    }
  });
  const res = await fetch(`${API_BASE}/cutoffs/neet?${searchParams.toString()}`);
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || 'Failed to search NEET cutoffs');
  }
  return res.json();
}

export async function searchUniversityCutoffs(params) {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') {
      searchParams.append(k, v);
    }
  });
  const res = await fetch(`${API_BASE}/cutoffs/university?${searchParams.toString()}`);
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || 'Failed to search university cutoffs');
  }
  return res.json();
}

export async function fetchGovernmentExams() {
  const res = await fetch(`${API_BASE}/career/gov-exams`);
  if (!res.ok) throw new Error('Failed to fetch government exams');
  return res.json();
}

export async function fetchContaminationReport() {
  const res = await fetch(`${API_BASE}/admin/contamination-test`);
  if (!res.ok) throw new Error('Failed to fetch contamination report');
  return res.json();
}

export async function fetchMedicalColleges(params = {}) {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v) searchParams.append(k, v);
  });
  const res = await fetch(`${API_BASE}/colleges/medical?${searchParams.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch medical colleges');
  return res.json();
}

export async function fetchUniversityColleges(params = {}) {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v) searchParams.append(k, v);
  });
  const res = await fetch(`${API_BASE}/colleges/university?${searchParams.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch university colleges');
  return res.json();
}

export async function fetchChatbotQuestions() {
  const res = await fetch(`${API_BASE}/chatbot/questions`);
  if (!res.ok) throw new Error('Failed to fetch chatbot questions');
  return res.json();
}

export async function recommendCareer(assessmentData) {
  const res = await fetch(`${API_BASE}/chatbot/recommend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(assessmentData)
  });
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || 'Failed to generate career recommendation');
  }
  return res.json();
}

export async function sendChatbotMessage(message, history = [], studentName = 'Student') {
  const res = await fetch(`${API_BASE}/chatbot/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message, history, student_name: studentName })
  });
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || 'Failed to get response from Margdarshak AI');
  }
  return res.json();
}

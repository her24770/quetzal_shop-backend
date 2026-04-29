// URL base del backend — viene del .env como VITE_API_URL
const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

// Helper genérico para llamadas autenticadas
export function apiFetch(path: string, token: string, options: RequestInit = {}) {
  return fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...(options.headers ?? {}),
    },
  });
}

// Llama a POST /auth/login y retorna el token + datos del usuario
export async function loginRequest(email: string, password: string) {
  const res = await fetch(`${BASE}/auth/login`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? 'Credenciales incorrectas');
  }

  return res.json();
}

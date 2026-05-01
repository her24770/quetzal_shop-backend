<script lang="ts">
  import { onMount } from 'svelte';
  import Icon from '$lib/components/Icon.svelte';
  import { IC } from '$lib/icons';
  import { auth } from '$lib/stores/auth';
  import { apiFetch } from '$lib/api';
  import { exportCsv } from '$lib/csv';

  interface Empleado {
    id: number; usuario_id: number; dpi: string; nombre: string;
    telefono: string; cargo: string; fecha_contrato: string;
    estado: string; email: string; rol_nombre: string;
  }

  let empleados: Empleado[] = [];
  let loading = true;
  let errorMsg = '';
  let saving = false;
  let formEl: HTMLElement;

  type Mode = 'add' | 'edit';
  let mode: Mode = 'add';
  let form = emptyForm();

  function emptyForm() {
    return { id: 0, usuario_id: '', dpi: '', nombre: '', telefono: '', cargo: '', fecha_contrato: '', estado: 'activo' };
  }

  $: isAdmin = $auth.user?.rol_id === 1;
  $: token   = $auth.token ?? '';

  onMount(async () => {
    const r = await apiFetch('/empleados', token);
    if (r.ok) empleados = await r.json();
    else errorMsg = 'Error al cargar empleados';
    loading = false;
  });

  async function reload() {
    const r = await apiFetch('/empleados', token);
    if (r.ok) empleados = await r.json();
  }

  function startEdit(e: Empleado) {
    form = {
      id: e.id, usuario_id: String(e.usuario_id), dpi: e.dpi,
      nombre: e.nombre, telefono: e.telefono, cargo: e.cargo,
      fecha_contrato: e.fecha_contrato, estado: e.estado,
    };
    mode = 'edit';
    errorMsg = '';
    setTimeout(() => formEl?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 0);
  }

  function cancelForm() {
    form = emptyForm();
    mode = 'add';
    errorMsg = '';
  }

  async function saveForm() {
    if (mode === 'add') {
      if (!form.usuario_id || !form.dpi || !form.nombre || !form.cargo || !form.fecha_contrato) {
        errorMsg = 'Completa todos los campos obligatorios'; return;
      }
      saving = true; errorMsg = '';
      const body = {
        usuario_id: parseInt(form.usuario_id), dpi: form.dpi, nombre: form.nombre,
        telefono: form.telefono, cargo: form.cargo, fecha_contrato: form.fecha_contrato,
      };
      try {
        const res = await apiFetch('/empleados', token, { method: 'POST', body: JSON.stringify(body) });
        if (!res.ok) { const e = await res.json().catch(() => ({})); errorMsg = e.detail ?? 'Error al guardar'; }
        else { await reload(); cancelForm(); }
      } finally { saving = false; }
    } else {
      saving = true; errorMsg = '';
      const body = { telefono: form.telefono, cargo: form.cargo, estado: form.estado };
      try {
        const res = await apiFetch(`/empleados/${form.id}`, token, { method: 'PATCH', body: JSON.stringify(body) });
        if (!res.ok) { const e = await res.json().catch(() => ({})); errorMsg = e.detail ?? 'Error al guardar'; }
        else { await reload(); cancelForm(); }
      } finally { saving = false; }
    }
  }

  async function deleteItem(id: number) {
    errorMsg = '';
    const res = await apiFetch(`/empleados/${id}`, token, { method: 'DELETE' });
    if (res.ok) {
      empleados = empleados.filter(e => e.id !== id);
      if (form.id === id) cancelForm();
    } else {
      const e = await res.json().catch(() => ({}));
      errorMsg = e.detail ?? 'Error al eliminar';
      setTimeout(() => formEl?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 0);
    }
  }

  function formatFecha(f: string) {
    return f ? new Date(f).toLocaleDateString('es-GT') : '—';
  }

  function exportarCSV() {
    exportCsv('empleados.csv',
      ['ID', 'Nombre', 'DPI', 'Cargo', 'Telefono', 'Email', 'Rol', 'Fecha Contrato', 'Estado'],
      empleados.map(e => [e.id, e.nombre, e.dpi, e.cargo, e.telefono, e.email, e.rol_nombre, e.fecha_contrato, e.estado])
    );
  }
</script>

<svelte:head><title>Empleados — QuetzalShop</title></svelte:head>

{#if isAdmin}
  <div class="form-card" bind:this={formEl}>
    <div class="form-card__header">
      <h3 class="form-card__title">{mode === 'add' ? 'Nuevo empleado' : 'Editar empleado'}</h3>
    </div>

    {#if errorMsg}
      <div class="form-error">{errorMsg}</div>
    {/if}

    <div class="form-grid">
      <!-- Campos solo visibles en modo agregar -->
      {#if mode === 'add'}
        <div class="qz-field">
          <label class="qz-label" for="e-uid">ID de usuario *</label>
          <input id="e-uid" type="number" class="qz-input" bind:value={form.usuario_id} placeholder="ID del usuario en el sistema" />
        </div>
        <div class="qz-field">
          <label class="qz-label" for="e-dpi">DPI *</label>
          <input id="e-dpi" class="qz-input" bind:value={form.dpi} placeholder="Número de DPI" />
        </div>
        <div class="qz-field">
          <label class="qz-label" for="e-nombre">Nombre completo *</label>
          <input id="e-nombre" class="qz-input" bind:value={form.nombre} placeholder="Nombre completo" />
        </div>
        <div class="qz-field">
          <label class="qz-label" for="e-fecha">Fecha de contrato *</label>
          <input id="e-fecha" type="date" class="qz-input" bind:value={form.fecha_contrato} />
        </div>
      {:else}
        <!-- En edición: nombre y DPI solo como referencia, deshabilitados -->
        <div class="qz-field">
          <label class="qz-label">Nombre</label>
          <input class="qz-input" value={form.nombre} disabled />
        </div>
        <div class="qz-field">
          <label class="qz-label">DPI</label>
          <input class="qz-input" value={form.dpi} disabled />
        </div>
      {/if}

      <!-- Campos editables siempre -->
      <div class="qz-field">
        <label class="qz-label" for="e-tel">Teléfono</label>
        <input id="e-tel" class="qz-input" bind:value={form.telefono} placeholder="5555-1234" />
      </div>
      <div class="qz-field">
        <label class="qz-label" for="e-cargo">Cargo *</label>
        <input id="e-cargo" class="qz-input" bind:value={form.cargo} placeholder="Cajero, Bodeguero, etc." />
      </div>

      {#if mode === 'edit'}
        <div class="qz-field">
          <label class="qz-label" for="e-estado">Estado</label>
          <select id="e-estado" class="qz-input" bind:value={form.estado}>
            <option value="activo">Activo</option>
            <option value="inactivo">Inactivo</option>
          </select>
        </div>
      {/if}
    </div>

    <div class="form-actions">
      {#if mode === 'edit'}
        <button class="btn btn-md btn-ghost" on:click={cancelForm}>Cancelar</button>
        <button class="btn btn-md btn-blue" on:click={saveForm} disabled={saving}>
          <Icon path={IC.check} size={13} /> {saving ? 'Guardando…' : 'Guardar cambios'}
        </button>
      {:else}
        <button class="btn btn-md btn-purple" on:click={saveForm} disabled={saving}>
          <Icon path={IC.plus} size={13} /> {saving ? 'Agregando…' : 'Agregar empleado'}
        </button>
      {/if}
    </div>
  </div>
{/if}

<div class="section-header">
  <h2 class="page-title">Empleados</h2>
  <button class="btn btn-sm btn-ghost" on:click={exportarCSV} disabled={empleados.length === 0}>
    <Icon path={IC.down} size={13} /> Exportar CSV
  </button>
</div>

{#if loading}
  <div class="loading-msg">Cargando empleados…</div>
{:else}
  <div class="qz-table-wrap">
    <table class="qz-table">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>DPI</th>
          <th>Cargo</th>
          <th>Teléfono</th>
          <th>Email</th>
          <th>Rol</th>
          <th>Contrato</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {#if empleados.length === 0}
          <tr class="empty-row"><td colspan="9">Sin empleados registrados</td></tr>
        {:else}
          {#each empleados as e}
            <tr class:row-selected={form.id === e.id && mode === 'edit'}>
              <td><span class="cell-main">{e.nombre}</span></td>
              <td><span class="cell-mono">{e.dpi}</span></td>
              <td>{e.cargo}</td>
              <td>{e.telefono}</td>
              <td><span class="cell-sub">{e.email}</span></td>
              <td>{e.rol_nombre}</td>
              <td>{formatFecha(e.fecha_contrato)}</td>
              <td>
                <span class="badge" class:badge-green={e.estado === 'activo'} class:badge-gray={e.estado !== 'activo'}>
                  {e.estado}
                </span>
              </td>
              <td>
                <div class="row-actions">
                  <button class="btn btn-sm btn-blue" on:click={() => startEdit(e)}>
                    <Icon path={IC.edit} size={11} /> Editar
                  </button>
                  <button class="btn btn-sm btn-danger" on:click={() => deleteItem(e.id)}>
                    <Icon path={IC.trash} size={11} /> Eliminar
                  </button>
                </div>
              </td>
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>
{/if}

<style>
  .form-card { background:#fff; border:1px solid #E5E7EB; border-radius:10px; padding:20px 24px; margin-bottom:24px; }
  .form-card__header { display:flex; align-items:center; justify-content:space-between; margin-bottom:16px; }
  .form-card__title { font-size:15px; font-weight:600; color:#111827; margin:0; }
  .form-error { background:#FEF2F2; border:1px solid #FECACA; color:#DC2626; font-size:13px; padding:8px 12px; border-radius:6px; margin-bottom:14px; }
  .form-grid { display:grid; grid-template-columns:1fr 1fr; gap:14px 20px; }
  .form-actions { display:flex; justify-content:flex-end; gap:10px; margin-top:16px; padding-top:14px; border-top:1px solid #F3F4F6; }
  .section-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; }
  .page-title { font-size:20px; font-weight:700; color:#111827; margin:0; }
  .loading-msg { color:#9CA3AF; font-size:14px; padding:20px 0; }
  .cell-main { font-weight:500; color:#111827; }
  .cell-sub  { font-size:12px; color:#6B7280; }
  .cell-mono { font-family:monospace; font-size:13px; }
  .row-actions { display:flex; gap:6px; }
  .row-selected td { background:#F5F3FF; }
  .badge { font-size:10px; font-weight:700; padding:2px 8px; border-radius:10px; }
  .badge-green { background:#D1FAE5; color:#065F46; }
  .badge-gray  { background:#F3F4F6; color:#6B7280; }
</style>

<script lang="ts">
  import { onMount } from 'svelte';
  import { auth } from '$lib/stores/auth';
  import { apiFetch } from '$lib/api';

  interface Compra {
    id: number; fecha: string; total: number; numero_factura: string; empleado: string;
  }

  let compras: Compra[] = [];
  let loading = true;
  let errorMsg = '';

  $: token = $auth.token ?? '';

  const fmt = (n: number) => 'Q ' + n.toLocaleString('es-GT', { minimumFractionDigits: 2 });
  function formatFecha(f: string) {
    return new Date(f).toLocaleDateString('es-GT', { year: 'numeric', month: 'short', day: 'numeric' });
  }

  onMount(async () => {
    const r = await apiFetch('/compras', token);
    if (r.ok) compras = await r.json();
    else errorMsg = 'Error al cargar compras';
    loading = false;
  });
</script>

<svelte:head><title>Compras — QuetzalShop</title></svelte:head>

<div class="section-header">
  <h2 class="page-title">Compras</h2>
</div>

{#if errorMsg}
  <div class="page-error">{errorMsg}</div>
{/if}

{#if loading}
  <div class="loading-msg">Cargando compras…</div>
{:else}
  <div class="qz-table-wrap">
    <table class="qz-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Fecha</th>
          <th>No. Factura</th>
          <th>Empleado</th>
          <th>Total</th>
        </tr>
      </thead>
      <tbody>
        {#if compras.length === 0}
          <tr class="empty-row"><td colspan="5">Sin compras registradas</td></tr>
        {:else}
          {#each compras as c}
            <tr>
              <td><span class="cell-id">#{c.id}</span></td>
              <td>{formatFecha(c.fecha)}</td>
              <td><span class="cell-mono">{c.numero_factura}</span></td>
              <td><span class="cell-sub">{c.empleado}</span></td>
              <td><span class="cell-total">{fmt(c.total)}</span></td>
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>
{/if}

<style>
  .section-header { margin-bottom:14px; }
  .page-title { font-size:20px; font-weight:700; color:#111827; margin:0; }
  .page-error { background:#FEF2F2; border:1px solid #FECACA; color:#DC2626; font-size:13px; padding:8px 12px; border-radius:6px; margin-bottom:14px; }
  .loading-msg { color:#9CA3AF; font-size:14px; padding:20px 0; }
  .cell-id    { font-family:monospace; color:#9CA3AF; font-size:12px; }
  .cell-sub   { font-size:12px; color:#6B7280; }
  .cell-mono  { font-family:monospace; font-size:13px; }
  .cell-total { font-weight:700; color:#111827; }
</style>

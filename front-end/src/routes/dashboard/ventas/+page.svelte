<script lang="ts">
  import { onMount } from 'svelte';
  import Icon from '$lib/components/Icon.svelte';
  import { IC } from '$lib/icons';
  import { auth } from '$lib/stores/auth';
  import { apiFetch } from '$lib/api';
  import { exportCsv } from '$lib/csv';

  interface Venta {
    id: number; fecha: string; total: number; descuento: number;
    cliente: string; nit: string; empleado: string; metodo_pago: string;
  }

  let ventas: Venta[] = [];
  let loading = true;
  let errorMsg = '';

  $: token = $auth.token ?? '';

  const fmt = (n: number) => 'Q ' + n.toLocaleString('es-GT', { minimumFractionDigits: 2 });
  function formatFecha(f: string) {
    return new Date(f).toLocaleDateString('es-GT', { year: 'numeric', month: 'short', day: 'numeric' });
  }

  onMount(async () => {
    const r = await apiFetch('/ventas', token);
    if (r.ok) ventas = await r.json();
    else errorMsg = 'Error al cargar ventas';
    loading = false;
  });

  function exportarCSV() {
    exportCsv('ventas.csv',
      ['ID', 'Fecha', 'Cliente', 'NIT', 'Empleado', 'Metodo Pago', 'Descuento', 'Total'],
      ventas.map(v => [v.id, v.fecha, v.cliente, v.nit, v.empleado, v.metodo_pago, v.descuento, v.total])
    );
  }
</script>

<svelte:head><title>Ventas — QuetzalShop</title></svelte:head>

<div class="section-header">
  <h2 class="page-title">Ventas</h2>
  <button class="btn btn-sm btn-ghost" on:click={exportarCSV} disabled={ventas.length === 0}>
    <Icon path={IC.down} size={13} /> Exportar CSV
  </button>
</div>

{#if errorMsg}
  <div class="page-error">{errorMsg}</div>
{/if}

{#if loading}
  <div class="loading-msg">Cargando ventas…</div>
{:else}
  <div class="qz-table-wrap">
    <table class="qz-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Fecha</th>
          <th>Cliente</th>
          <th>NIT</th>
          <th>Empleado</th>
          <th>Método pago</th>
          <th>Descuento</th>
          <th>Total</th>
        </tr>
      </thead>
      <tbody>
        {#if ventas.length === 0}
          <tr class="empty-row"><td colspan="8">Sin ventas registradas</td></tr>
        {:else}
          {#each ventas as v}
            <tr>
              <td><span class="cell-id">#{v.id}</span></td>
              <td>{formatFecha(v.fecha)}</td>
              <td><span class="cell-main">{v.cliente}</span></td>
              <td><span class="cell-mono">{v.nit}</span></td>
              <td><span class="cell-sub">{v.empleado}</span></td>
              <td>{v.metodo_pago}</td>
              <td>{v.descuento > 0 ? fmt(v.descuento) : '—'}</td>
              <td><span class="cell-total">{fmt(v.total)}</span></td>
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>
{/if}

<style>
  .section-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; }
  .page-title { font-size:20px; font-weight:700; color:#111827; margin:0; }
  .page-error { background:#FEF2F2; border:1px solid #FECACA; color:#DC2626; font-size:13px; padding:8px 12px; border-radius:6px; margin-bottom:14px; }
  .loading-msg { color:#9CA3AF; font-size:14px; padding:20px 0; }
  .cell-id    { font-family:monospace; color:#9CA3AF; font-size:12px; }
  .cell-main  { font-weight:500; color:#111827; }
  .cell-sub   { font-size:12px; color:#6B7280; }
  .cell-mono  { font-family:monospace; font-size:13px; }
  .cell-total { font-weight:700; color:#111827; }
</style>

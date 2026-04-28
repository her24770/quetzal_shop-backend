<script lang="ts">
  import { auth } from '$lib/stores/auth';
  $: user = $auth.user;
</script>

<div class="page-header">
  <h1 class="page-title">Dashboard</h1>
  <p class="page-sub">Bienvenido, {user?.nombre_empleado ?? user?.email}</p>
</div>

<style>
  .page-header { margin-bottom: 24px; }
  .page-title  { font-size: 22px; font-weight: 700; color: var(--g-900); margin: 0 0 4px; }
  .page-sub    { font-size: 14px; color: var(--g-400); margin: 0; }
</style>

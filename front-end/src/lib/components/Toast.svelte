<script lang="ts">
  import Icon from './Icon.svelte';
  import { IC } from '$lib/icons';

  export let toasts: { id: number; msg: string; type: 'success' | 'error' }[] = [];

  function dismiss(id: number) {
    toasts = toasts.filter(t => t.id !== id);
  }
</script>

<div class="toast-container">
  {#each toasts as t (t.id)}
    <div class="toast {t.type}">
      <Icon path={t.type === 'error' ? IC.alert : IC.check} size={15} />
      <span class="toast-msg">{t.msg}</span>
      <button class="toast-close" on:click={() => dismiss(t.id)}>
        <Icon path={IC.x} size={13} />
      </button>
    </div>
  {/each}
</div>

<script lang="ts">
  export let path: string;
  export let size: number = 16;
  export let strokeWidth: number = 1.8;
  export let color: string = 'currentColor';
</script>

<svg
  width={size}
  height={size}
  viewBox="0 0 24 24"
  fill="none"
  stroke={color}
  stroke-width={strokeWidth}
  stroke-linecap="round"
  stroke-linejoin="round"
  style="display:block;flex-shrink:0"
>
  <path d={path} />
</svg>

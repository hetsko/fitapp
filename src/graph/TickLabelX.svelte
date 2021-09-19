<script>
    import { formatNumber } from "./ticks";
    import { toClientX, toClientY, clientHeight } from "./storeTransforms";

    export let x;
    export let base = 0;
    export let baseFormatted = null;
    export let zeroThr = 0;

    $: yRaw = $toClientY(0);
    $: y = Math.max(Math.min(yRaw, 0), -$clientHeight);
    $: flipped = y > 0.1 * -$clientHeight;
</script>

<text
    x={$toClientX(x) + 8}
    y={y + (flipped ? -8 : +4)}
    text-anchor="start"
    dominant-baseline={flipped ? "bottom" : "hanging"}
>
    {#if Math.abs(base) >= zeroThr && y !== yRaw}
        {baseFormatted ?? base} +
    {/if}
    {#if Math.abs(x - base) >= zeroThr}
        {formatNumber(x - base)}
    {:else}
        0.00
    {/if}
</text>

<script>
    import { formatNumber } from "./ticks";
    import { toClientX, toClientY, clientWidth } from "../store";

    export let y;
    export let base = 0;
    export let baseFormatted = null;
    export let zeroThr = 0;

    $: xRaw = $toClientX(0);
    $: x = Math.min(Math.max(xRaw, 0), $clientWidth);
    $: flipped = x < 0.1 * $clientWidth;
</script>

<text
    x={x + (flipped ? +8 : -8)}
    y={$toClientY(y) + 4}
    text-anchor={flipped ? "start" : "end"}
    dominant-baseline="hanging"
>
    {#if Math.abs(base) >= zeroThr && x !== xRaw}
        {baseFormatted ?? base}
        {y - base >= 0 ? " + " : " + ("}
        {#if Math.abs(y - base) >= zeroThr}
            {formatNumber(y - base)}
        {/if}
        {y - base >= 0 ? "" : ")"}
    {:else if Math.abs(y - base) >= zeroThr}
        {formatNumber(y - base)}
    {:else}
        0.00
    {/if}
</text>

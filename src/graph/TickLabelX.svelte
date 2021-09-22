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

    let text;
    $: if (Math.abs(base) >= zeroThr && y !== yRaw) {
        text = `${baseFormatted ?? base}`;
        if (Math.abs(x - base) >= zeroThr) {
            text +=
                x - base >= 0
                    ? ` + ${formatNumber(x - base)}`
                    : ` + (${formatNumber(x - base)})`;
        }
    } else if (Math.abs(x - base) >= zeroThr) {
        text = formatNumber(x - base);
    } else {
        text = "0.00";
    }
</script>

<text
    x={$toClientX(x) + 8}
    y={y + (flipped ? -8 : +4)}
    text-anchor="start"
    dominant-baseline={flipped ? "bottom" : "hanging"}
>
    {text}
</text>

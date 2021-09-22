<script>
    import { formatNumber } from "./ticks";
    import { toClientX, toClientY, clientWidth } from "./storeTransforms";

    export let y;
    export let base = 0;
    export let baseFormatted = null;
    export let zeroThr = 0;

    $: xRaw = $toClientX(0);
    $: x = Math.min(Math.max(xRaw, 0), $clientWidth);
    $: flipped = x < 0.1 * $clientWidth;

    let text;
    $: if (Math.abs(base) >= zeroThr && x !== xRaw) {
        text = `${baseFormatted ?? base}`;
        if (Math.abs(y - base) >= zeroThr) {
            text +=
                y - base >= 0
                    ? ` + ${formatNumber(y - base)}`
                    : ` + (${formatNumber(y - base)})`;
        }
    } else if (Math.abs(y - base) >= zeroThr) {
        text = formatNumber(y - base);
    } else {
        text = "0.00";
    }
</script>

<text
    x={x + (flipped ? +8 : -8)}
    y={$toClientY(y) + 4}
    text-anchor={flipped ? "start" : "end"}
    dominant-baseline="hanging"
    transform={`rotate(${x !== xRaw ? 30 : 0}, ${
        x + (flipped ? +8 : -8)
    }, ${$toClientY(y)})`}
>
    {text}
</text>

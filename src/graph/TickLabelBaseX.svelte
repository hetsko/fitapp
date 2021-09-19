<script>
    import { beforeUpdate } from "svelte";
    import { toClientY } from "./storeTransforms";

    export let base;
    export let baseFormatted = null;

    let textElem;
    let bbox;

    beforeUpdate(() => {
        bbox = textElem?.getBBox() ?? { x: 0, y: 0, width: 0, height: 0 };
    });
</script>

<rect
    fill="#e0e0e0"
    x={0}
    y={$toClientY(0) - (bbox.height + 8)}
    width={bbox.width + 16}
    height={bbox.height + 8}
/>
<text x={8} y={$toClientY(0) - 8} text-anchor="start" bind:this={textElem}>
    {baseFormatted ?? base} +
</text>

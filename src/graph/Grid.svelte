<script>
    import LineH from "./LineH.svelte";
    import LineV from "./LineV.svelte";
    import TickLabelX from "./TickLabelX.svelte";
    import TickLabelY from "./TickLabelY.svelte";
    import TickLabelBaseX from "./TickLabelBaseX.svelte";
    import TickLabelBaseY from "./TickLabelBaseY.svelte";
    import {
        getTicks,
        getMinorTick,
        getTicksBase,
        formatNumberToDelta,
    } from "./ticks";
    import { xLim, yLim, gridParams } from "../storeConfiguration";
    import { toClientX, toClientY } from "./storeTransforms";

    $: xTicksMajor = getTicks(...$xLim);
    $: yTicksMajor = getTicks(...$yLim);
    $: xTicksMinor = getMinorTick(xTicksMajor);
    $: yTicksMinor = getMinorTick(yTicksMajor);

    $: xBase = getTicksBase(xTicksMajor);
    $: yBase = getTicksBase(yTicksMajor);

    $: yDelta = yTicksMajor[1] - yTicksMajor[0];
    $: xDelta = xTicksMajor[1] - xTicksMajor[0];
</script>

<g>
    {#if $gridParams.minor}
        <g stroke="#e0e0e0">
            {#each xTicksMinor as x}
                <LineV x={$toClientX(x)} />
            {/each}
            {#each yTicksMinor as y}
                <LineH y={$toClientY(y)} />
            {/each}
        </g>
    {/if}
    {#if $gridParams.major}
        <g stroke="#808080">
            {#each xTicksMajor as x}
                <LineV x={$toClientX(x)} />
            {/each}
            {#each yTicksMajor as y}
                <LineH y={$toClientY(y)} />
            {/each}
        </g>
    {/if}
    {#if $gridParams.axes}
        <g stroke="black">
            <LineH y={$toClientY(0)} lw="2" />
            <LineV x={$toClientX(0)} lw="2" />
        </g>
    {/if}
    {#if $gridParams.major}
        <g>
            {#if xBase !== 0}
                <TickLabelBaseX
                    base={xBase}
                    baseFormatted={formatNumberToDelta(xBase, xDelta)}
                />
            {/if}
            {#each xTicksMajor as x}
                {#if Math.abs(x) >= 0.5 * xDelta}
                    <TickLabelX
                        {x}
                        base={xBase}
                        zeroThr={0.5 * xDelta}
                        baseFormatted={formatNumberToDelta(xBase, xDelta)}
                    />
                {/if}
            {/each}
            {#if yBase !== 0}
                <TickLabelBaseY
                    base={yBase}
                    baseFormatted={formatNumberToDelta(yBase, yDelta)}
                />
            {/if}
            {#each yTicksMajor as y}
                {#if Math.abs(y) >= 0.5 * yDelta}
                    <TickLabelY
                        {y}
                        base={yBase}
                        zeroThr={0.5 * yDelta}
                        baseFormatted={formatNumberToDelta(yBase, yDelta)}
                    />
                {/if}
            {/each}
            <TickLabelY y={0} zeroThr={0.5 * yDelta} />
        </g>
    {/if}
</g>

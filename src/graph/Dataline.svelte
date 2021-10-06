<script>
    import { draw, fade } from "svelte/transition";
    import { clientHeight, toClientX, toClientY } from "./storeTransforms";

    export let data;
    export let selected = null;

    export let noMarker = false;
    export let noLine = false;
    export let noAnimation = false;

    export let params = {};
    params = {
        color: "red",
        // mec: ,
        // mfc: ,
        markersize: 5,
        // lc: ,
        lw: 2,
        ...params,
    };

    $: lineString =
        noLine || data.x.length === 0
            ? ""
            : data.hasOwnProperty("y")
            ? data.x.reduce(
                  (path, x, i) =>
                      path + ` ${$toClientX(x)},${$toClientY(data.y[i])}`,
                  `M ${$toClientX(data.x[0])},${$toClientY(data.y[0])} L`
              )
            : data.x.reduce(
                  (path, x) =>
                      path + `M ${$toClientX(x)},0 v -${$clientHeight}`,
                  ""
              );
</script>

<g>
    {#if !noLine}
        <g
            fill="none"
            stroke={params.lc ?? params.color}
            stroke-width={params.lw}
            stroke-dasharray={params.ls === "--"
                ? 8
                : params.ls === ":"
                ? 2
                : "none"}
        >
            <path
                d={lineString}
                in:draw={{ duration: !noAnimation ? 500 : 0 }}
            />
        </g>
    {/if}
    {#if !noMarker && data.hasOwnProperty("y") && data.hasOwnProperty("yerr")}
        <g
            fill={params.mfc ?? params.color}
            stroke={params.mec ?? params.color}
        >
            {#each data.x as x, i}
                <line
                    x1={$toClientX(x)}
                    x2={$toClientX(x)}
                    y1={$toClientY(data.y[i] - data.yerr[i])}
                    y2={$toClientY(data.y[i] + data.yerr[i])}
                />
            {/each}
        </g>
    {/if}
    {#if !noMarker && data.hasOwnProperty("y")}
        <g
            fill={params.mfc ?? params.color}
            stroke={params.mec ?? params.color}
        >
            {#each data.x as x, i}
                <circle
                    cx={$toClientX(x)}
                    cy={$toClientY(data.y[i])}
                    r={params.markersize}
                    {...selected && selected.has(i) ? { fill: "black" } : {}}
                />
            {/each}
        </g>
    {/if}
</g>

<style>
    /* svg {
        transform: scaleY(-1);
    } */
</style>

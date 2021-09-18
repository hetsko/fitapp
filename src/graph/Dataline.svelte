<script>
    import { toClientX, toClientY } from "../store";

    export let data;
    export let selected;

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

    $: pointsString = data.x.reduce(
        (path, x, i) => path + ` ${$toClientX(x)},${$toClientY(data.y[i])}`,
        ""
    );
</script>

<g>
    <g fill="none" stroke={params.lc ?? params.color} stroke-width={params.lw}>
        <polyline points={pointsString} />
    </g>
    <g fill={params.mfc ?? params.color} stroke={params.mec ?? params.color}>
        {#each data.x as x, i}
            <circle
                cx={$toClientX(x)}
                cy={$toClientY(data.y[i])}
                r={params.markersize}
                {...selected.has(i) ? { fill: "black" } : {}}
            />
        {/each}
    </g>
</g>

<style>
    /* svg {
        transform: scaleY(-1);
    } */
</style>

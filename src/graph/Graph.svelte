<script>
    import Grid from "./Grid.svelte";
    import Dataline from "./Dataline.svelte";
    import { data, selected, fitGuess } from "../storeData";
    import { clientWidth, clientHeight } from "./storeTransforms";
    import { fetchFitData } from "../requests";

    const num = 500;
    $: start = $data.x.at($selected.size ? Math.min(...$selected) : 0);
    $: stop = $data.x.at($selected.size ? Math.max(...$selected) : -1);
</script>

<div class="root" on:mousedown on:mousewheel>
    <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 {-$clientHeight} {$clientWidth} {$clientHeight}"
    >
        <Grid />
        {#if $data.x.length > 0}
            <Dataline data={$data} selected={$selected} noLine />
            {#if $fitGuess}
                {#await fetchFitData($fitGuess, start, stop, num) then fitdata}
                    <Dataline
                        data={fitdata}
                        noMarker
                        params={{ color: "green" }}
                    />
                {/await}
            {/if}
        {/if}
    </svg>
</div>

<style>
    svg {
        stroke: black;
        font-weight: 100;
    }
    .root {
        height: 50%;
    }
</style>

<script>
    import Grid from "./Grid.svelte";
    import Dataline from "./Dataline.svelte";
    import { dataSorted, selected } from "../storeData";
    import { clientWidth, clientHeight } from "./storeTransforms";
</script>

<div class="root" on:mousedown on:mousewheel>
    <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 {-$clientHeight} {$clientWidth} {$clientHeight}"
    >
        <Grid />
        <Dataline data={$dataSorted} selected={$selected} />
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

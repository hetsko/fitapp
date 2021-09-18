<script>
    import Grid from "./Grid.svelte";
    import Dataline from "./Dataline.svelte";
    import { clientWidth, clientHeight, dataSorted, selected } from "../store";
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
        height: 100%;
    }
</style>

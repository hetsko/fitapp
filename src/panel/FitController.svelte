<script>
    import { fetchFitResults } from "../requests";
    import {
        idSelected,
        fitMetadata,
        fitGuess,
        fitResults,
    } from "../storeData";
</script>

<div>
    {#each $fitMetadata.params as param}
        <label for="fit-param-{param}">{param}</label>
        <input id="fit-param-{param}" type="range" />
    {/each}
    <br />
    <button
        on:click={() =>
            fetchFitResults($idSelected, $fitGuess).then(
                results => ($fitResults = results)
            )}>Fit data</button
    >
</div>

<style>
    span {
        margin: 0.5em;
    }
</style>

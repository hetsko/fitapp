<script>
    import { fetchFitResults } from "../requests";
    import { formatNumber } from "../graph/ticks";
    import {
        idSelected,
        fitMetadata,
        fitGuess,
        fitResults,
    } from "../storeData";

    $: min = $fitMetadata.args.map(a => (a !== 0 ? 0.5 * a : -10));
    $: max = $fitMetadata.args.map(a => (a !== 0 ? 1.5 * a : +10));

    const handleArgChange = i => e => {
        $fitGuess = [
            ...$fitGuess.slice(0, i),
            Number(e.target.value),
            ...$fitGuess.slice(i + 1),
        ];
    };
</script>

<div>
    {#each $fitMetadata.params as param, i}
        <div class="container">
            <label for="fit-param-{param}">
                {param}={formatNumber($fitGuess[i])}
            </label>
            <input
                on:input={handleArgChange(i)}
                id="fit-param-{param}"
                min={min[i]}
                max={max[i]}
                step="any"
                type="range"
            />
        </div>
    {/each}
    <button
        on:click={() =>
            fetchFitResults($idSelected, $fitGuess).then(
                results => ($fitResults = results)
            )}>Fit data</button
    >
</div>

<style>
    .container {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    label {
        margin-right: 0.4em;
    }
</style>

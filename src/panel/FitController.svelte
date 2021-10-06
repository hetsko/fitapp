<script>
    import { formatNumber } from "../graph/ticks";
    import { fitMetadata, fitGuess } from "../storeData";
    import { fitEnabled } from "../storeConfiguration";

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
    Fit data
    <input
        class="toggle"
        type="checkbox"
        min="0"
        max="1"
        on:change={e => ($fitEnabled = e.target.checked)}
    />
</div>

<style>
    label {
        margin-right: 0.4em;
    }
    .container {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    input.toggle {
        appearance: none;
        position: relative;
        width: 2rem;
        height: 1rem;
        padding: 0;
        margin: auto;
    }
    input.toggle:hover {
        background-color: #ccc;
    }
    input.toggle::before {
        content: "";
        display: block;
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 50%;
        background-color: #777;
        border-radius: 2px;
        transition: left 0.2s, right 0.2s;
    }
    input.toggle:checked::before {
        background-color: lightcoral;
        left: 50%;
        right: 0;
        transition: left 0.2s, right 0.2s;
    }
</style>

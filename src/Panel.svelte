<script>
    import { createEventDispatcher } from "svelte";
    import { formatNumber } from "./graph/ticks";
    import { xLim, yLim, gridParams } from "./store";

    let dispatch = createEventDispatcher();

    let [setXLimMin, setXLimMax] = [0, 0];
    let [setYLimMin, setYLimMax] = [0, 0];

    xLim.subscribe(lim => {
        const relLimWidth =
            (Math.abs(lim[1]) + Math.abs(lim[0])) / (lim[1] - lim[0]);
        const digits = Math.max(3, Math.ceil(Math.log10(relLimWidth)) + 1);
        setXLimMin = formatNumber(lim[0], digits);
        setXLimMax = formatNumber(lim[1], digits);
    });
    yLim.subscribe(lim => {
        const relLimWidth =
            (Math.abs(lim[1]) + Math.abs(lim[0])) / (lim[1] - lim[0]);
        const digits = Math.max(3, Math.ceil(Math.log10(relLimWidth)) + 1);
        setYLimMin = formatNumber(lim[0], digits);
        setYLimMax = formatNumber(lim[1], digits);
    });
</script>

<aside>
    <h1>&quot;A nice day to fit.&quot;</h1>
    <div class="container">
        <!-- <input type="range" min="1" max="10" bind:value={graphWidth} /> -->
        <!-- <input type="number" on:submit="{(e) => graph.setXLim(value)}" /> -->
        <div>
            <input type="text" step="any" bind:value={setXLimMin} />
            &leq; x &leq;
            <input type="text" step="any" bind:value={setXLimMax} />
            <button
                on:click={() =>
                    xLim.set([Number(setXLimMin), Number(setXLimMax)])}
            >
                Set
            </button>
        </div>

        <div>
            <input type="text" step="any" bind:value={setYLimMin} />
            &leq; y &leq;
            <input type="text" step="any" bind:value={setYLimMax} />
            <button
                on:click={() =>
                    yLim.set([Number(setYLimMin), Number(setYLimMax)])}
            >
                Set
            </button>
        </div>

        <div>
            <button on:click={() => dispatch("resetlims")}>Reset</button>
            <br />
            {#each ["major", "minor"] as param}
                {param} ticks
                <input
                    type="checkbox"
                    checked={$gridParams[param]}
                    on:change={e => {
                        gridParams.update(params => ({
                            ...params,
                            [param]: e.target.checked,
                        }));
                    }}
                />
                <br />
            {/each}
        </div>
    </div>
</aside>

<style>
    aside {
        text-align: center;
        position: absolute;
        right: 0;
        top: 0;
        padding: 1rem;
        max-width: 20rem;
        background-color: #efefefe0;
    }
    h1 {
        /* color: #ff3e00; */
        text-transform: uppercase;
        font-size: 3.2rem;
        font-weight: 100;
        font-family: Cambria, Cochin, Georgia, Times, "Times New Roman", serif;
    }

    input {
        max-width: 12ch;
        /* margin: 0 2rem; */
    }
    .container {
        display: flex;
        flex-direction: column;
        /* flex-wrap: wrap; */
        justify-content: center;
        /* max-width: 16rem; */
    }
</style>

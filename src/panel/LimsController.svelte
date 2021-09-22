<script>
    import { createEventDispatcher } from "svelte";
    import { formatNumber } from "../graph/ticks";
    import { xLim, yLim } from "../storeConfiguration";

    let [setXLimMin, setXLimMax] = [0, 0];
    let [setYLimMin, setYLimMax] = [0, 0];

    function getDigits(lim) {
        const relLimWidth =
            (Math.abs(lim[1]) + Math.abs(lim[0])) / (lim[1] - lim[0]);
        return Math.max(3, Math.ceil(Math.log10(relLimWidth)) + 1);
    }

    xLim.subscribe(lim => {
        const digits = getDigits(lim);
        setXLimMin = formatNumber(lim[0], digits);
        setXLimMax = formatNumber(lim[1], digits);
    });
    yLim.subscribe(lim => {
        const digits = getDigits(lim);
        setYLimMin = formatNumber(lim[0], digits);
        setYLimMax = formatNumber(lim[1], digits);
    });

    let dispatch = createEventDispatcher();
</script>

<div>
    <input type="text" step="any" bind:value={setXLimMin} />
    &leq; x &leq;
    <input type="text" step="any" bind:value={setXLimMax} />
    <button on:click={() => xLim.set([Number(setXLimMin), Number(setXLimMax)])}>
        Set
    </button>
    <br />

    <input type="text" step="any" bind:value={setYLimMin} />
    &leq; y &leq;
    <input type="text" step="any" bind:value={setYLimMax} />
    <button on:click={() => yLim.set([Number(setYLimMin), Number(setYLimMax)])}>
        Set
    </button>
    <br />

    <button on:click={() => dispatch("resetlims")}>Reset</button>
</div>

<style>
    input {
        max-width: 12ch;
        /* margin: 0 2rem; */
    }
</style>

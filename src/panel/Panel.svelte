<script>
    import { cubicOut } from "svelte/easing";
    import IdSelector from "./IdSelector.svelte";
    import LimsController from "./LimsController.svelte";
    import GridController from "./GridController.svelte";
    import FitController from "./FitController.svelte";
    import ChevronRight from "svelte-icons/fa/FaChevronRight.svelte";
    import ChevronLeft from "svelte-icons/fa/FaChevronLeft.svelte";

    let visible = true;

    function slideRight(node, params) {
        const existingTransform = getComputedStyle(node).transform.replace(
            "none",
            ""
        );

        return {
            delay: params.delay || 0,
            duration: params.duration || 300,
            easing: params.easing || cubicOut,
            css: (t, u) =>
                `transform: ${existingTransform} translate(${
                    (1 - t) * node.clientWidth
                }px, 0)`,
        };
    }
</script>

{#if visible}
    <aside transition:slideRight>
        <button
            class="hide-button"
            on:click={() => (visible = false)}
            aria-label="Hide panel"
        >
            <ChevronRight />
        </button>
        <h1>&quot;A nice day to fit.&quot;</h1>
        <div class="container">
            <IdSelector />
            <hr />
            <FitController />
            <hr />
            <LimsController on:resetlims />
            <hr />
            <GridController />
        </div>
    </aside>
{:else}
    <button
        class="show-button"
        in:slideRight={{ delay: 300 }}
        on:click={() => (visible = true)}
        aria-label="Show panel"
    >
        <ChevronLeft />
    </button>
{/if}

<style>
    aside {
        text-align: center;
        position: absolute;
        right: 0;
        top: 0;
        bottom: 0;
        padding: 2rem 0.5rem;
        width: clamp(16rem, 25vw, 32rem);
        background-color: #efefefe0;
        display: flex;
        flex-direction: column;
    }
    h1 {
        text-transform: uppercase;
        font-size: 3.2rem;
        font-weight: 100;
        font-family: Cambria, Cochin, Georgia, Times, "Times New Roman", serif;
    }

    .show-button,
    .hide-button,
    .show-button:hover,
    .hide-button:hover {
        position: absolute;
        top: 0;
        width: 4em;
        height: 4em;
        background-color: #00000000;
    }
    .show-button:not(:focus),
    .hide-button:not(:focus) {
        border: hidden;
    }
    .show-button {
        right: 0;
    }
    .hide-button {
        right: 0;
    }
    .show-button:not(:disabled):hover,
    .hide-button:not(:disabled):hover {
        color: #666;
    }

    .container {
        display: block;
        flex-direction: column;
        /* flex-wrap: wrap; */
        justify-content: center;
        /* max-width: 16rem; */
        overflow-y: auto;
        /* height: 100%; */
        padding: 0rem 1rem;
    }
    hr {
        width: 100%;
        border: unset;
        border-top: #ccc solid 3px;
        margin: 1rem 0rem;
        /* border-radius: 4px; */
    }
</style>

<script>
    import { ids, idSelected } from "../storeData";
</script>

<div>
    {#each $ids as id}
        <button
            disabled={id === $idSelected}
            value={id}
            on:click={e => {
                $idSelected = e.target.value;
            }}
        >
            {id}
        </button>
    {/each}
</div>

<style>
    button {
        margin: 0.2em;
    }
    button:disabled {
        background-color: lightcoral;
        color: white;
    }
</style>

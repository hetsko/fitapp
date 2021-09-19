<script>
    import { ids, idSelected } from "../storeData";
</script>

<div class="root">
    {#each $ids as id}
        <button
            disabled={id === $idSelected}
            on:click={e => {
                $idSelected = e.target.innerText;
            }}>{id}</button
        >
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

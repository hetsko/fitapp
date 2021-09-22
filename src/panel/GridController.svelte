<script>
    import { gridParams } from "../storeConfiguration";
</script>

<div>
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

<style>
</style>

<script>
    import IdSelector from "./IdSelector.svelte";
    import LimsController from "./LimsController.svelte";
    import GridController from "./GridController.svelte";
    import FitController from "./FitController.svelte";
</script>

<aside>
    <h1>&quot;A nice day to fit.&quot;</h1>
    <div class="container">
        <IdSelector />
        <LimsController on:resetlims />
        <GridController />
        <FitController />
    </div>
</aside>

<style>
    aside {
        text-align: center;
        position: absolute;
        right: 0;
        top: 0;
        padding: 2rem 1rem;
        max-width: 20rem;
        background-color: #efefefe0;
    }
    h1 {
        text-transform: uppercase;
        font-size: 3.2rem;
        font-weight: 100;
        font-family: Cambria, Cochin, Georgia, Times, "Times New Roman", serif;
    }

    .container {
        display: flex;
        flex-direction: column;
        /* flex-wrap: wrap; */
        justify-content: center;
        /* max-width: 16rem; */
    }
</style>

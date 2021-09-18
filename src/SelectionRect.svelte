<script>
    export let rect;
    export let variant;
</script>

<div
    style="
        left: {rect.x + Math.min(0, rect.width)}px;
        top: {rect.y + Math.min(0, rect.height)}px;
        width: {Math.abs(rect.width)}px;
        height: {Math.abs(rect.height)}px;

    "
    class="variant{variant}"
/>

<style>
    div {
        position: absolute;
    }
    .variant0 {
        border: 2px solid #a0a0f0;
        background-color: #a0a0f070;
    }
    .variant1 {
        border: 2px solid #c0c0c0;
        background-color: #c0c0c070;
    }
</style>

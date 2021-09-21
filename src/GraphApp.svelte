<script>
    import Graph from "./graph/Graph.svelte";
    import SelectionRect from "./SelectionRect.svelte";
    import Panel from "./panel/Panel.svelte";
    import {
        clientWidth,
        clientHeight,
        toPlotX,
        toPlotY,
        toPlotScaleX,
        toPlotScaleY,
    } from "./graph/storeTransforms";
    import { data, selected } from "./storeData";
    import { xLim, yLim } from "./storeConfiguration";
    import { formatNumber } from "./graph/ticks";

    function setDefaultLims(data) {
        if (data.x.length !== 0) {
            const xMin = Math.min(...data.x);
            const dx = Math.max(...data.x) - xMin;
            $xLim = [xMin - 0.1 * dx, xMin + 1.1 * dx];

            const yMin = Math.min(...data.y);
            const dy = Math.max(...data.y) - yMin;
            if (data.hasOwnProperty("y") && dy > 0) {
                $yLim = [yMin - 0.1 * dy, yMin + 1.1 * dy];
            } else {
                $yLim = [-10, 10];
            }
        } else {
            $xLim = [-10, 10];
            $yLim = [-10, 10];
        }
    }
    $: setDefaultLims($data);

    function pointsInRect(dataX, dataY, bboxClient) {
        const bbox = {
            x: $toPlotX(bboxClient.x),
            y: $toPlotY(bboxClient.y),
            width: $toPlotScaleX(bboxClient.width),
            height: $toPlotScaleY(bboxClient.height),
        };

        const results = new Set();
        const checkPoint = (x, y) =>
            Math.abs(x - (bbox.x + 0.5 * bbox.width)) <
                Math.abs(0.5 * bbox.width) &&
            Math.abs(y - (bbox.y + 0.5 * bbox.height)) <
                Math.abs(0.5 * bbox.height);

        const binarySearch = (arr, x) => {
            if (x < arr.at(0)) return 0;
            if (x > arr.at(-1)) return arr.length;
            let left = 0;
            let right = arr.length;
            let i;
            while (left + 1 < right) {
                i = Math.floor(0.5 * (left + right));
                if (x < arr[i]) right = i;
                else left = i;
            }
            return right;
        };

        const iMin = binarySearch(dataX, bbox.x + Math.min(bbox.width, 0));
        const iMax = binarySearch(dataX, bbox.x + Math.max(bbox.width, 0));
        for (let i = iMin; i < iMax; i++) {
            if (checkPoint(dataX[i], dataY[i])) results.add(i);
        }
        return results;
    }

    //
    // User interaction
    //

    let mouseAction = "none";
    let mouseActionRect = { x: 0, y: 0, width: 0, height: 0 };
    let mousePlotCoords = { x: 0, y: 0 };

    let cursor = "default";
    function handleKey(e) {
        if (e.type === "keydown") {
            if (e.key === "Escape") cancelAction();
            else if (e.key === "Control") cursor = "zoom-in";
            else if (e.key === "Shift") cursor = "crosshair";
        } else {
            if (e.key === "Control") cancelAction(["rectZoom"]);
            else if (e.key === "Shift") cancelAction(["rectSelect"]);
            cursor = "default";
        }
    }

    function handleMouseDown(e) {
        if (e.button === 0) {
            if (e.ctrlKey && e.shiftKey) {
                mouseAction = "???";
            } else if (e.ctrlKey) {
                mouseActionRect = {
                    x: e.clientX,
                    y: e.clientY,
                    width: 0,
                    height: 0,
                };
                mouseAction = "rectZoom";
            } else if (e.shiftKey) {
                mouseActionRect = {
                    x: e.clientX - 2, // 2px shift so that the crosshair cursor
                    y: e.clientY - 2, // is aligned with the rect's border
                    width: 0,
                    height: 0,
                };
                mouseAction = "rectSelect";
            } else {
                mouseAction = "grab";
            }
            // Prevent text selection (tick labels, etc.)
            e.preventDefault();
        }
    }

    function handleMouseMove(e) {
        switch (mouseAction) {
            case "grab":
                xLim.update(lim => [
                    lim[0] + $toPlotScaleX(-e.movementX),
                    lim[1] + $toPlotScaleX(-e.movementX),
                ]);
                yLim.update(lim => [
                    lim[0] + $toPlotScaleY(-e.movementY),
                    lim[1] + $toPlotScaleY(-e.movementY),
                ]);
                break;
            case "rectZoom":
            case "rectSelect":
                mouseActionRect = {
                    ...mouseActionRect,
                    width: mouseActionRect.width + e.movementX,
                    height: mouseActionRect.height + e.movementY,
                };
                break;
            case "none":
            default:
                mousePlotCoords = {
                    x: $toPlotX(e.clientX),
                    y: $toPlotY(e.clientY),
                };
        }
    }

    function finishAction(actions) {
        if (actions && !actions.includes(mouseAction)) return;

        switch (mouseAction) {
            case "rectZoom":
                const { x, y, width, height } = mouseActionRect;
                $xLim = [
                    $toPlotX(x + Math.min(0, width)),
                    $toPlotX(x + Math.max(0, width)),
                ];
                $yLim = [
                    $toPlotY(y + Math.max(0, height)),
                    $toPlotY(y + Math.min(0, height)),
                ];
                break;
            case "rectSelect":
                $selected = pointsInRect($data.x, $data.y, mouseActionRect);
                break;
        }
        mouseAction = "none";
    }

    function cancelAction(actions) {
        if (actions && !actions.includes(mouseAction)) return;
        mouseAction = "none";
    }

    function handleWheel(e) {
        const pivotXY = {
            x: $toPlotX(e.clientX),
            y: $toPlotY(e.clientY),
        };
        const scale = 1 + e.deltaY / 1000;

        function transform(pivot, x) {
            return pivot + scale * (x - pivot);
        }
        xLim.update(lim => [
            transform(pivotXY.x, lim[0]),
            transform(pivotXY.x, lim[1]),
        ]);
        yLim.update(lim => [
            transform(pivotXY.y, lim[0]),
            transform(pivotXY.y, lim[1]),
        ]);
    }
</script>

<svelte:window on:keydown={handleKey} on:keyup={handleKey} />

<div
    on:mouseleave={() => cancelAction(["grab"])}
    on:mouseup={() => finishAction()}
    on:mousemove={handleMouseMove}
    bind:clientWidth={$clientWidth}
    bind:clientHeight={$clientHeight}
    class="root"
    style="cursor: {cursor};"
>
    <Graph on:mousedown={handleMouseDown} on:mousewheel={handleWheel} />
    {#if mouseAction.startsWith("rect")}
        <SelectionRect
            variant={mouseAction === "rectZoom" ? 0 : 1}
            rect={mouseActionRect}
        />
    {/if}
    <Panel on:resetlims={setDefaultLims($data)} />
    <div class="mouse-position">
        [{formatNumber(mousePlotCoords.x)},
        {formatNumber(mousePlotCoords.y)}]
    </div>
</div>

<style>
    .root {
        height: 100%;
        position: relative;
    }
    .mouse-position {
        position: absolute;
        bottom: 1rem;
        right: 2rem;
        text-align: right;
    }
</style>

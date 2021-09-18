import { writable, derived, readable } from "svelte/store";
import { absolute, relative } from "./graph/transforms";

export const clientWidth = writable(1);
export const clientHeight = writable(1);

//
// Data
//

export const data = readable({ x: [], y: [] }, set => {
    // set({
    //     x: [34, 10, 20, 30, 40, 50],
    //     y: [0, 12, 33, 35, 45, 32],
    // });

    const dataY = [
        3606, 3606, 3606, 3883, 3883, 4376, 4556, 4556, 4902, 5080, 5080, 5512,
        6118, 6118, 6322, 6322, 6786, 7141, 7141, 7428, 7945, 8321, 9102, 9322,
        9322, 9668, 9668, 9668, 9668, 10010, 10276, 10623, 10623, 10623, 10623,
        10623, 10851, 11007, 11007, 11007, 11007, 11007, 11127, 11193, 11443,
        11468, 11468, 11468, 11468, 11468, 11468, 11468, 11468, 11468, 11468,
        11468, 11468, 11841, 11841, 11841, 11841, 11841, 11841, 11841, 12200,
        12501, 12501, 12501, 12944, 13180, 13180, 13180, 13180, 13180, 13180,
        13180, 13180, 13180, 13180, 13581, 13800, 13800, 13800, 13800, 13911,
        14409, 14409, 14409, 14409, 14409, 14409, 14395, 14562, 14562, 14562,
        14562, 14562, 14562, 14562, 14984, 14984, 14984, 14984, 14984, 14984,
        14984, 14984, 15548, 15940, 15940, 16206, 16363, 16363, 16363, 16721,
        16721, 17150, 17684, 17684, 17984, 18530, 18956, 18956, 18956, 18956,
    ];
    set({
        x: dataY.map((_y, i) => i),
        y: dataY,
    });
});
export const dataSorted = derived(data, $data => {
    const sorted = $data.x
        .map((x, i) => ({ x, y: $data.y[i] }))
        .sort((a, b) => a.x - b.x);
    return { x: sorted.map(a => a.x), y: sorted.map(b => b.y) };
});

export const selected = writable(new Set());
// export const selected = derived(data, $data => $data.x.map(() => false));

//
// Params
//

export const xLim = writable([0, 1]);
export const yLim = writable([0, 1]);

export const gridParams = writable({
    minor: true,
    major: true,
    axes: true,
});

//
// Derived: Transform calculations
//

export const toClientX = derived([clientWidth, xLim], args =>
    absolute.toClientX(...args)
);
export const toClientY = derived([clientHeight, yLim], args =>
    absolute.toClientY(...args)
);
export const toPlotX = derived([clientWidth, xLim], args =>
    absolute.toPlotX(...args)
);
export const toPlotY = derived([clientHeight, yLim], args =>
    absolute.toPlotY(...args)
);

export const toClientScaleX = derived([clientWidth, xLim], args =>
    relative.toClientX(...args)
);
export const toClientScaleY = derived([clientHeight, yLim], args =>
    relative.toClientY(...args)
);
export const toPlotScaleX = derived([clientWidth, xLim], args =>
    relative.toPlotX(...args)
);
export const toPlotScaleY = derived([clientHeight, yLim], args =>
    relative.toPlotY(...args)
);

import { writable, derived } from "svelte/store";
import { absolute, relative } from "./transforms";

import { xLim, yLim } from "../storeConfiguration";

export const clientWidth = writable(1);
export const clientHeight = writable(1);

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

import { writable } from "svelte/store";

export const xLim = writable([0, 1]);
export const yLim = writable([0, 1]);

export const gridParams = writable({
    minor: true,
    major: true,
    axes: true,
});

export const fitEnabled = writable(false);

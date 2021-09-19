import { writable, derived, readable } from "svelte/store";
import { fetchIds, fetchMetadata, fetchData } from "./fetchData";

export const ids = readable([], set => {
    fetchIds().then(a => set(a));
});

export const idSelected = writable(null);

//
// Data
//

export const metadata = derived(
    idSelected,
    ($id, set) => {
        fetchMetadata($id).then(a => set(a));
    },
    "..."
);

export const data = derived(
    idSelected,
    ($id, set) => {
        if ($id) fetchData($id).then(data => set(data));
    },
    { x: [] }
);

export const dataSorted = derived(data, $data => {
    const keys = Object.keys($data);
    if (keys.every(k => ["x"].includes(k))) {
        return { x: [...$data.x].sort((a, b) => a.x - b.x) };
    } else if (keys.every(k => ["x", "y"].includes(k))) {
        const sorted = $data.x
            .map((x, i) => ({ x, y: $data.y[i] }))
            .sort((a, b) => a.x - b.x);
        return { x: sorted.map(a => a.x), y: sorted.map(b => b.y) };
    } else if (keys.every(k => ["x", "y", "yerr"].includes(k))) {
        const sorted = $data.x
            .map((x, i) => ({ x, y: $data.y[i], yerr: $data.yerr[i] }))
            .sort((a, b) => a.x - b.x);
        return {
            x: sorted.map(a => a.x),
            y: sorted.map(b => b.y),
            yerr: sorted.map(b => b.yerr),
        };
    } else {
        console.error(`Data format {${keys}} not implemented`);
        return { x: [] };
    }
});

export const selected = writable(new Set());
// export const selected = derived(data, $data => $data.x.map(() => false));

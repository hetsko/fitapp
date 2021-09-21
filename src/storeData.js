import { writable, derived, readable } from "svelte/store";
import { fetchIds, fetchMetadata, fetchData } from "./requests";

export const ids = readable([], set => {
    fetchIds().then(a => set(a));
});

export const idSelected = writable(null);

export const fitGuess = readable([1, 2, 3]);

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

export const selected = writable(new Set());
// export const selected = derived(data, $data => $data.x.map(() => false));

import { writable, derived, readable } from "svelte/store";
import {
    fetchIds,
    fetchMetadata,
    fetchData,
    fetchFitMetadata,
} from "./requests";

export const ids = readable([], set => {
    fetchIds().then(a => {
        set(a);
        idSelected.set(a[0] ?? null);
    });
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

export const selected = writable(new Set());
// export const selected = derived(data, $data => $data.x.map(() => false));

//
// Fit
//

export const fitMetadata = derived(
    idSelected,
    ($id, set) => {
        if ($id)
            fetchFitMetadata($id).then(data => {
                set(data);
                fitGuess.set(data.args);
            });
    },
    { args: [], params: [] }
);

export const fitGuess = writable(null);

import { writable, derived, readable } from "svelte/store";
import {
    fetchIds,
    fetchMetadata,
    fetchData,
    fetchFitMetadata,
    fetchFitResults,
} from "./requests";
import { fitEnabled } from "./storeConfiguration";

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
        if ($id) fetchMetadata($id).then(a => set(a));
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
        if ($id) fetchFitMetadata($id).then(data => set(data));
    },
    { args: [], params: [] }
);

export const fitGuess = (() => {
    const store = writable(null);
    fitMetadata.subscribe($metadata => store.set($metadata.args));
    return store;
})();

// export const fitResults = (() => {
//     const store = writable(null);
//     fitMetadata.subscribe(() => store.set(null));
//     return store;
// })();

export const fitResults = derived(
    [idSelected, fitGuess, selected, fitEnabled],
    ([$idSelected, $fitGuess, $selected, $fitEnabled], set) => {
        if ($idSelected && $fitGuess && $fitEnabled) {
            fetchFitResults($idSelected, $fitGuess, [...$selected]).then(
                results => set(results)
            );
        } else {
            set(null);
        }
    }
);

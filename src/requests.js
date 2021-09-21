async function checkAndHandleError(response, label) {
    if (!response.ok) {
        try {
            const data = await response.json();
            console.error(
                `${label} error: ${data.error} ${data.exception ?? ""}`
            );
        } catch (error) {
            console.error(
                `${label} error ${response.status} (no json in response)`
            );
        }
        return true;
    }
    return false;
}

function sortData(data) {
    const keys = Object.keys(data);
    if (keys.every(k => ["x"].includes(k))) {
        return { x: [...data.x].sort((a, b) => a.x - b.x) };
    } else if (keys.every(k => ["x", "y"].includes(k))) {
        const sorted = data.x
            .map((x, i) => ({ x, y: data.y[i] }))
            .sort((a, b) => a.x - b.x);
        return { x: sorted.map(a => a.x), y: sorted.map(b => b.y) };
    } else if (keys.every(k => ["x", "y", "yerr"].includes(k))) {
        const sorted = data.x
            .map((x, i) => ({ x, y: data.y[i], yerr: data.yerr[i] }))
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
}

export async function fetchIds() {
    const response = await fetch("/ids");
    if (await checkAndHandleError(response, "fetchIds()")) return [];

    const { ids } = await response.json();
    return ids;
}

export async function fetchMetadata(id) {
    const response = await fetch("/data/meta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id }),
    });
    if (await checkAndHandleError(response, "fetchMetadata()")) return "[n/a]";

    const { metadata } = await response.json();
    return metadata;
}

export async function fetchData(id) {
    const response = await fetch("/data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id }),
    });
    if (await checkAndHandleError(response, "fetchData()")) return { x: [] };

    const { data } = await response.json();
    if (data.y && data.y.length !== data.x.length) {
        console.error(
            `Data id='${id}' has mismatched dimensions (x[${data.x.length}], y[${data.y.length}])`
        );
    }
    if (data.yerr && data.yerr.length !== data.x.length) {
        console.error(
            `Data id='${id}' has mismatched dimensions (x[${data.x.length}], yerr[${data.yerr.length}])`
        );
    }
    return sortData(data);
}

export async function fetchFitMetadata(id) {
    const response = await fetch("/fit/meta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id }),
    });
    if (await checkAndHandleError(response, "fetchFitMetadata()"))
        return "[n/a]";

    const { metadata } = await response.json();
    return metadata;
}

export async function fetchFitData(fitArgs, start, stop, num) {
    const response = await fetch("/fit/data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fitArgs, start, stop, num }),
    });
    if (await checkAndHandleError(response, "fetchFitData()"))
        return { x: [], y: [] };

    const { data } = await response.json();
    if (data.y && data.y.length !== data.x.length) {
        console.error(
            `Fitdata has mismatched dimensions (x[${data.x.length}], y[${data.y.length}])`
        );
    }
    if (data.yerr && data.yerr.length !== data.x.length) {
        console.error(
            `Fitdata has mismatched dimensions (x[${data.x.length}], yerr[${data.yerr.length}])`
        );
    }
    return sortData(data);
}
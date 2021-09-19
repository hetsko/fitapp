async function checkAndHandleError(response, label) {
    if (!response.ok) {
        try {
            const data = await response.json();
            console.error(`${label} error: ${data.error}`);
        } catch (error) {
            console.error(
                `${label} error ${response.status} (no json in response)`
            );
        }
        return true;
    }
    return false;
}

export async function fetchIds() {
    const response = await fetch("/ids");
    if (await checkAndHandleError(response, "fetchIds()")) return [];

    const { ids } = await response.json();
    return ids;
}

export async function fetchMetadata(id) {
    const response = await fetch("/metadata", {
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
    return data;
}

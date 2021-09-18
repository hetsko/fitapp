//
// Format numbers
//

export function formatNumber(number, digits = 3) {
    /*
        Format `number` to fixed/exp depending on what is more appropriate.
    */
    return Math.abs(number) >= 0.1
        ? number.toPrecision(digits)
        : number.toExponential(digits - 1);
}

export function formatNumberToDelta(number, delta) {
    /*
        Format `number` with sufficient precision in respect to `delta`.
        e.g. (1001.000000, 0.1) => "1001.0"
    */
    const digits =
        Math.floor(Math.log10(number)) - Math.floor(Math.log10(delta)) + 1;
    return digits >= 1 && digits < 100 ? number.toPrecision(digits) : null;
}

//
// Tick calculations
//

export function getTicks(limMin, limMax) {
    /*
        Calculate evenly spaced ticks with constraints:
            - spacing 1, 2, 5, 10, 20, 50 etc.
            - at least 3 ticks inside the (limMin, limMax) interval
    */
    const log = Math.log10((limMax - limMin) / 3);

    const logFloor = Math.floor(log);
    const logFrac = log - logFloor;

    let dx;
    if (logFrac > 0.69897) {
        // === log10(5)
        dx = Math.pow(10, logFloor + 0.69897);
    } else if (logFrac > 0.30103) {
        // === log10(2)
        dx = Math.pow(10, logFloor + 0.30103);
    } else {
        dx = Math.pow(10, logFloor);
    }

    // Subtracting single dx to include additional tick before limMin,
    // useful for getMinorTick()
    let tick = Math.ceil(limMin / dx) * dx - dx;
    const ticks = [];
    while (tick < limMax) {
        ticks.push(tick);
        tick += dx;
    }
    return ticks;
}

export function getMinorTick(major) {
    /*
        Calculate minor ticks from major ticks with 1/5th spacing.
    */
    const dx = (major[1] - major[0]) / 5;
    return major.reduce((arr, tick) => {
        for (let i = 0; i < 5; i++) arr.push(tick + i * dx);
        return arr;
    }, []);
}

function floorAbs(a, digit) {
    const scale = Math.pow(10, digit);
    return Math.sign(a) * Math.floor(Math.abs(a) / scale) * scale;
}

export function getTicksBase(ticks, formatDigits = 3) {
    // We are trying to avoid "bad tick" =
    //   Adjacent tick labels are formatted to strings represented equal
    //   numbers, when formatted with precision given by `formatDigits`.
    //     e.g. 21.02 21.04 21.06 ----> "21.0" "21.0" "21.1"

    //   We can prevent that by subtracting an appropriate `base` number.
    //     e.g. base=20, then display "20 + 1.02"

    const threshold = Math.floor(
        Math.log10(ticks[1] - ticks[0]) + formatDigits
    );

    // Largest tick (in abs. value) is used to calculate the base.
    // The resulting base might be actually 0, which indicates that no
    // transformation of the ticks is needed.
    if (ticks.at(0) > 0) {
        const base = floorAbs(ticks.at(-1), threshold);
        return base;
        return [base, Math.max(1, threshold)];
    } else {
        const base = floorAbs(ticks.at(0), threshold);
        return base;
        return [base, Math.max(1, threshold)];
    }
}

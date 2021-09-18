//
// Absolute coordinates (points)
//
export const absolute = {
    toClientX: (clientWidth, xLim) => plotX =>
        ((plotX - xLim[0]) / (xLim[1] - xLim[0])) * clientWidth,

    toClientY: (clientHeight, yLim) => plotY =>
        -((plotY - yLim[0]) / (yLim[1] - yLim[0])) * clientHeight,

    toPlotX: (clientWidth, xLim) => clientX =>
        (clientX / clientWidth) * (xLim[1] - xLim[0]) + xLim[0],

    toPlotY: (clientHeight, yLim) => clientY =>
        ((clientHeight - clientY) / clientHeight) * (yLim[1] - yLim[0]) +
        yLim[0],
};

//
// Relative coordinates (e.g. distances)
//

export const relative = {
    toClientX: (clientWidth, xLim) => plotX =>
        (plotX / (xLim[1] - xLim[0])) * clientWidth,

    toClientY: (clientHeight, yLim) => plotY =>
        -(plotY / (yLim[1] - yLim[0])) * clientHeight,

    toPlotX: (clientWidth, xLim) => clientX =>
        (clientX / clientWidth) * (xLim[1] - xLim[0]),

    toPlotY: (clientHeight, yLim) => clientY =>
        -(clientY / clientHeight) * (yLim[1] - yLim[0]),
};

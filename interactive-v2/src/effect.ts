import { Frame } from "./mini-vinci";

export function pixelate(frame: Frame, factor: number): Frame {
    const result: Frame = [];
    for (let i = 0; i < 400 * 400; i++) {
        result.push({ r: 255, g: 255, b: 255, a: 255 });
    }

    for (let y = 0; y < 400; y += factor) {
        for (let x = 0; x < 400; x += factor) {
            let r = 0;
            let g = 0;
            let b = 0;
            let a = 0;
            for (let yy = y; yy < y + factor; yy++) {
                for (let xx = x; xx < x + factor; xx++) {
                    let px = frame[yy * 400 + xx];
                    if (px) {
                        r += px.r;
                        g += px.g;
                        b += px.b;
                        a += px.a;
                    }
                }
            }

            r /= factor * factor;
            g /= factor * factor;
            b /= factor * factor;
            a /= factor * factor;

            r = Math.max(0, Math.min(255, Math.round(r)));
            g = Math.max(0, Math.min(255, Math.round(g)));
            b = Math.max(0, Math.min(255, Math.round(b)));
            a = Math.max(0, Math.min(255, Math.round(a)));

            for (let yy = y; yy < y + factor; yy++) {
                for (let xx = x; xx < x + factor; xx++) {
                    result[yy * 400 + xx] = {
                        r,
                        g,
                        b,
                        a,
                    };
                }
            }
        }
    }
    return result;
}

import { inverseLerp } from "three/src/math/MathUtils.js";
import { LDN_NE_BOUNDARY, LDN_SW_BOUNDARY, SCALE_FACTOR } from "./constants";

export const ASPECT_RATIO = (LDN_NE_BOUNDARY[0] - LDN_SW_BOUNDARY[0]) / (LDN_NE_BOUNDARY[1] - LDN_SW_BOUNDARY[1])

export function MapLocationInLondon(x, y) {
    var mapped_x = inverseLerp(LDN_SW_BOUNDARY[0], LDN_NE_BOUNDARY[0], x) * SCALE_FACTOR;
    var mapped_y = inverseLerp(LDN_NE_BOUNDARY[1], LDN_SW_BOUNDARY[1], y) * SCALE_FACTOR / ASPECT_RATIO;
    return [mapped_x, mapped_y];
}

import * as THREE from 'three'


export const SCALE_FACTOR = 10;
export const ORBIT = true;
export const DEBUG_LIGHTS = false;

export const COLOR_MAP = {
    "E": new THREE.Color(0xFFE9D0),   // peach
    "EC": new THREE.Color(0xFFFED3),  // yellow
    "N": new THREE.Color(0xBBE9FF),  // blue
    "NW": new THREE.Color(0xB1AFFF),  // purple
    "SE": new THREE.Color(0xBAD8B6),  // green
    "SW": new THREE.Color(0xFFD2A0),  // orange
    "W": new THREE.Color(0xE16A54),  // maroon
    "WC": new THREE.Color(0xEFB6C8),  // pink
}

export const LDN_SW_BOUNDARY = [515000.0, 165000.0]
export const LDN_NE_BOUNDARY = [550000.0, 200000.0]

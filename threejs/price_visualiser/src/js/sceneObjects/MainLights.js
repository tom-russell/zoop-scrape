import * as THREE from 'three'
import { DEBUG_LIGHTS } from '../constants';

export class MainLights {
    constructor(scene) {
        const ambientLight = new THREE.AmbientLight(0xFFFFFF, 0.5);
        const directionalLight = new THREE.DirectionalLight(0xFFFFFF, 1.5);
        directionalLight.position.x = 1;
        directionalLight.position.y = 5;
        directionalLight.position.z = 2;

        if (DEBUG_LIGHTS) {
            const helper = new THREE.DirectionalLightHelper(directionalLight, 5);
            scene.add(helper);
        }

        scene.add(ambientLight, directionalLight);
    }

    update() { }
} 
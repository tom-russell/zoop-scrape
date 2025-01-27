import * as THREE from 'three'


export class Grid {
    constructor(scene) {
        this.gridHelper = new THREE.GridHelper(100, 50);
        scene.add(this.gridHelper);
    }

    update() { }
}
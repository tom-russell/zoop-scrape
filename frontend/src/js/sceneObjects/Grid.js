import * as THREE from 'three'


export class Grid {
    constructor(scene) {
        this.gridHelper = new THREE.GridHelper(10, 10);
        this.gridHelper.position.set(5, 0, 5);
        scene.add(this.gridHelper);
    }

    update() { }
}
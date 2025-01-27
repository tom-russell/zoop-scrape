import * as THREE from 'three'
import { COLOR_MAP } from '../constants';
import { MapLocationInLondon } from '../utils';


var jsonData = await getSaleData();


export class PropertySaleData {
    constructor(scene) {
        this.materialMap = {};
        for (const [areaCode, color] of Object.entries(COLOR_MAP)) {
            this.materialMap[areaCode] = new THREE.MeshStandardMaterial({ color: color });
        }

        for (var i = 0; i < jsonData.length; i++)
            this.addSale(scene, jsonData[i]);
    }

    addSale(scene, saleData) {
        var price_scale = saleData["price_gbp"] / 2000000;
        var shortCode = saleData["short_code"].replace(/\d.*/, '')
        const box = new THREE.Mesh(
            new THREE.BoxGeometry(0.1, price_scale, 0.1, 1, 1, 1),
            this.materialMap[shortCode],
        );
        var [x, y] = MapLocationInLondon(saleData["bng_coordinate_x"], saleData["bng_coordinate_y"]);
        box.position.set(x, price_scale / 2, y);
        scene.add(box);
    }

    update(elapsedTime) { }
}


async function getSaleData() {
    const url = "http://127.0.0.1:8000/sales";
    try {
        const response = await fetch(url + "?count=3000");
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        const json = await response.json();
        console.log(json)
        return json;
    } catch (error) {
        console.error(error.message);
    }
}


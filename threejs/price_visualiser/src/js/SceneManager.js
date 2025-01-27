import { Grid } from "./sceneObjects/Grid";
import * as THREE from 'three';
import { ORBIT, SCALE_FACTOR } from "./constants";
import { PropertySaleData } from "./sceneObjects/PropertySaleData";
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { MainLights } from "./sceneObjects/MainLights";


export class SceneManager {
    constructor(canvas) {
        this.clock = new THREE.Clock();
        this.canvas = canvas;

        const screenDimensions = {
            width: canvas.width,
            height: canvas.height
        }

        this.scene = this.buildScene();
        this.renderer = this.buildRender(screenDimensions);
        this.camera = this.buildCamera(screenDimensions);
        this.sceneObjects = this.createSceneObjects(this.scene);
    }

    buildScene() {
        const scene = new THREE.Scene();
        scene.background = new THREE.Color("#000");

        return scene;
    }

    buildRender() {
        const renderer = new THREE.WebGLRenderer({ canvas })
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(window.innerWidth, window.innerHeight);
        return renderer;
    }

    buildCamera() {
        var camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();

        camera.rotation.set(-Math.PI / 2, 0, 0);
        camera.position.set(SCALE_FACTOR / 2, 15, SCALE_FACTOR / 2);
        return camera;
    }
    createSceneObjects(scene) {
        var objects = [
            new Grid(scene),
            new PropertySaleData(scene),
            new MainLights(scene),
        ];
        if (ORBIT) {
            this.controls = new OrbitControls(this.camera, this.renderer.domElement);
            objects.push(this.controls);
        }
        return objects;
    }

    update() {
        const elapsedTime = this.clock.getElapsedTime();

        for (let i = 0; i < this.sceneObjects.length; i++)
            this.sceneObjects[i].update(elapsedTime);

        if (this.controls)
            this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }

    onWindowResize() {
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
    }
}
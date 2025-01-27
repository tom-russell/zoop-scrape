import { SceneManager } from "./SceneManager";
import "../style.css";

const canvas = document.getElementById("canvas");

const sceneManager = new SceneManager(canvas);

bindEventListeners();
render();


function bindEventListeners() {

    window.addEventListener('resize', setCanvasSize);
}

function setCanvasSize() {
    sceneManager.onWindowResize();
}
setCanvasSize()

function render() {
    requestAnimationFrame(render);
    sceneManager.update();
}

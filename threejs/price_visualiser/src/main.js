import { inverseLerp, lerp } from 'three/src/math/MathUtils.js';
import './style.css'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';


const ORBIT = true;
const SCALE_FACTOR = 10;

const colorMap = {
  "E": new THREE.Color(0xFFE9D0),   // peach
  "EC": new THREE.Color(0xFFFED3),  // yellow
  "N": new THREE.Color(0xBBE9FF),  // blue
  "NW": new THREE.Color(0xB1AFFF),  // purple
  "SE": new THREE.Color(0xBAD8B6),  // green
  "SW": new THREE.Color(0xFFD2A0),  // orange
  "W": new THREE.Color(0xE16A54),  // maroon
  "WC": new THREE.Color(0xEFB6C8),  // pink
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

const LDN_SW_BOUNDARY = [515000.0, 165000.0]
const LDN_NE_BOUNDARY = [550000.0, 200000.0]

const ASPECT_RATIO = (LDN_NE_BOUNDARY[0] - LDN_SW_BOUNDARY[0]) / (LDN_NE_BOUNDARY[1] - LDN_SW_BOUNDARY[1])
function mapLocationInLondon(x, y) {
  var mapped_x = inverseLerp(LDN_SW_BOUNDARY[0], LDN_NE_BOUNDARY[0], x) * SCALE_FACTOR;
  var mapped_y = inverseLerp(LDN_NE_BOUNDARY[1], LDN_SW_BOUNDARY[1], y) * SCALE_FACTOR / ASPECT_RATIO;
  return [mapped_x, mapped_y];
}


var jsonData = await getSaleData();


const canvas = document.querySelector('#bg')
const renderer = new THREE.WebGLRenderer({ canvas })
const scene = new THREE.Scene();
var camera =  new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.rotation.set(-Math.PI / 2, 0, 0);
camera.position.set(SCALE_FACTOR / 2, 15, SCALE_FACTOR / 2);

function setCanvasSize() {
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
}
window.addEventListener('resize', setCanvasSize);
setCanvasSize()

var controls = null
if (ORBIT) {
  controls = new OrbitControls(camera, renderer.domElement);
}

function addCorner(xBng, yBng, color) {
  const box = new THREE.Mesh(
    new THREE.CylinderGeometry(0.2, 0.2, 0.5),
    new THREE.MeshStandardMaterial({ color: color })
  );
  var [x, y] = mapLocationInLondon(xBng, yBng);
  box.position.set(x, 0.25, y);
  scene.add(box);
}
addCorner(529393, 178960, 0xFF00FF);  // coburg close, purple
addCorner(533862, 184920, 0xFFFF00);  // dalston
addCorner(534474, 179372, 0xFF0000); // bermondsey, red
addCorner(531973, 174573, 0xFFFFFF); // herne hill


function addSale(saleData) {
  var price_scale = saleData["price_gbp"] / 2000000;
  var color = colorMap[saleData["short_code"].replace(/\d.*/, '')]
  const box = new THREE.Mesh(
    new THREE.BoxGeometry(0.1, price_scale, 0.1, 1, 1, 1),
    new THREE.MeshStandardMaterial({ color: color })
  );
  var [x, y] = mapLocationInLondon(saleData["bng_coordinate_x"], saleData["bng_coordinate_y"]);
  box.position.set(x, price_scale / 2, y);
  scene.add(box);
}

for (var i = 0; i < jsonData.length; i++) {
  addSale(jsonData[i]);
}


function addLightsAndGrid() {
  const gridHelper = new THREE.GridHelper(100, 50);
  scene.add(gridHelper);

  const ambientLight = new THREE.AmbientLight(0xFFFFFF, 0.5);
  const directionalLight = new THREE.DirectionalLight(0xFFFFFF, 1.5);
  directionalLight.position.x = 1
  directionalLight.position.y = 5

  directionalLight.position.z = 2
  scene.add(ambientLight, directionalLight);
  // const helper = new THREE.DirectionalLightHelper( directionalLight, 5 );
  // scene.add( helper );
}

addLightsAndGrid();

function animate() {
  requestAnimationFrame(animate);

  if (ORBIT) {
    controls.update();
  }

  renderer.render(scene, camera);
}

animate();
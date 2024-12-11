let blockImg;
let block1;
let block2;
let clack = new Audio('clack.wav');;
let runAnim = false;

let count = 0;
let digits = 7;
let countDiv;
const timeSteps = 10 ** (digits - 1);

function setup() {
  createCanvas(800, 300);
  block1 = new Block(100, 50, 1, 0, 0);
  const m2 = pow(100, digits - 1);
  block2 = new Block(200, 100, m2, -1 / timeSteps, 20);
}

function draw() {
  background(1000);

  let clackSound = false;

  for (let i = 0; i < timeSteps; i++) {
    if (!runAnim) continue;
    if (block1.collide(block2)) {
      const v1 = block1.bounce(block2);
      const v2 = block2.bounce(block1);
      block1.v = v1;
      block2.v = v2;
      clackSound = true;
      count++;
    }

    if (block1.hitWall()) {
      block1.reverse();
      clackSound = true;
      count++;
    }

    block1.update();
    block2.update();
  }

  if (clackSound) {
    clack.play();
  }
  block1.show();
  block2.show();

  fill('black');
  text(`Collisions: ${count}`, 5, 15);
}

function play() {
  runAnim = true;
  count = 0;
  digits = parseInt(document.getElementById('digits').value);
  setup();
}
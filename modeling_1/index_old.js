const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
clack = new Audio('clack.wav');

let collisions = 0;

class Object {

  constructor(x, v, m, s, c = "black") {
    this.x = x;
    this.vel = v;
    this.mass = m;
    this.size = s;
    this.color = c;
  }

  update() {
    this.x += this.vel;

    if (this.x <= 0) {
      collisions++;
      this.vel = -this.vel;
    }
  }

  draw() {
    let old = ctx.fillStyle;
    ctx.fillStyle = this.color;

    ctx.beginPath()
    ctx.fillRect(this.x, canvas.height - this.size, this.size, this.size)
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = old;



    ctx.font = "10px helvetica";
    ctx.fillText(`mass: ${this.mass}`, this.x, canvas.height - this.size * 1.25)
    ctx.fillText(`velocity: ${this.vel.toFixed(2)}`, this.x, canvas.height - this.size * 1.5)
  }
}

let object1 = new Object(100, 0, 1, 50, "yellow");
let object2 = new Object(200, -1, 10000, 50, "orange");
let stop_animation = false;

function checkCollision(object1, object2) {
  // Calculate the right edge of each object
  let rightEdgeObject1 = object1.x + object1.size;
  let rightEdgeObject2 = object2.x + object2.size;

  // Check if object1's right edge has passed object2's left edge and vice versa
  if (rightEdgeObject1 >= object2.x && object1.x <= rightEdgeObject2) {
      // Play collision sound
      clack.play();

      // Calculate the new velocities after collision
      let newVelObject1 = ((object1.mass - object2.mass) * object1.vel + 2 * object2.mass * object2.vel) / (object1.mass + object2.mass);
      let newVelObject2 = ((object2.mass - object1.mass) * object2.vel + 2 * object1.mass * object1.vel) / (object1.mass + object2.mass);

      // Update velocities
      object1.vel = newVelObject1;
      object2.vel = newVelObject2;

      // Increment collision count
      collisions++;
  }
}

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  object1.update();
  object1.draw();

  object2.update();
  object2.draw();

  checkCollision(object1, object2);

  ctx.font = "10px helvetica";
  ctx.fillText(`collsions: ${collisions}`, 10, 20);

  if (!stop_animation) requestAnimationFrame(animate);
  // setTimeout(() => animate(), 1)
}

function play() {
  animate();
}

object1.draw();
object2.draw();
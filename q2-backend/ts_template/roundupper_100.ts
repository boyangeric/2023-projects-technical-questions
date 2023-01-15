import express from "express";

// location is the simple (x, y) coordinates of an entity within the system
// spaceCowboy models a cowboy in our super amazing system
// spaceAnimal models a single animal in our amazing system
type location = { x: number; y: number };
type spaceCowboy = { name: string; lassoLength: number };
type spaceAnimal = { type: "pig" | "cow" | "flying_burger" };

// spaceEntity models an entity in the super amazing (ROUND UPPER 100) system
type spaceEntity =
  | { type: "space_cowboy"; metadata: spaceCowboy; location: location }
  | { type: "space_animal"; metadata: spaceAnimal; location: location };

type animalsType = { type: "pig" | "cow" | "flying_burger", location: location}[]

// === ADD YOUR CODE BELOW :D ===

// === ExpressJS setup + Server setup ===
const spaceDatabase = [] as spaceEntity[];
const app = express();
app.use(express.json())
// the POST /entity endpoint adds an entity to your global space database
app.post("/entity", (req, res) => {
  const data = req.body;
  spaceDatabase.concat(data);
  return res.status(200).json({});
});

// /lassoable returns all the space animals a space cowboy can lasso given their name
app.get("/lassoable", (req, res) => {
  const { cowboy_name } = req.query;
  let animals: animalsType = [];
  let lassoLength: number = 0;
  let x_c: number = 0;
  let y_c: number = 0;
  for (const entity of spaceDatabase) {
    if (
      entity.type === "space_cowboy" &&
      entity.metadata.name === cowboy_name
    ) {
      lassoLength = entity.metadata.lassoLength;
      x_c = entity.location.x;
      y_c = entity.location.y;
    }
    if (entity.type === "space_animal") {
      const x_a = entity.location.x;
      const y_a = entity.location.y;
      const distance = Math.sqrt((x_c - x_a) ** 2 + (y_c - y_a) ** 2);
      if (distance <= lassoLength) {
        animals.push({ type: entity.metadata.type, location: entity.location });
      }
    }
  }
  return res.status(200).json({space_animals: animals})
});

app.listen(8080);

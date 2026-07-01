import sharp from "sharp";
import fs from "fs";

const files = fs.readdirSync("./../public/assets")
  .filter(file => !file.endsWith(".webp")); // 👈 clé du fix

for (const file of files) {
  const name = file.split(".")[0];

  await sharp(`./../public/assets/${file}`)
    .webp({ quality: 80 })
    .toFile(`./../public/assets/${name}.webp`);

  console.log(`${file} converti`);
}
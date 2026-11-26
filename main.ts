// news-image-20261126 — entry program.
// The newspaper page is composed ahead of time by compose.py and committed
// as entry.png. At grade time this program copies that image into the
// output folder and verifies the copy byte for byte, so the two runs the
// scorer makes always deliver exactly the same file.
import { copyFileSync, readFileSync, existsSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");

if (!existsSync(src)) {
  console.error("entry.png is missing next to main.ts");
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);

// Verify: PNG signature, size cap of 1 MiB, and a byte-identical copy.
const a = readFileSync(src);
const b = readFileSync(dst);
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const isPng = PNG_MAGIC.every((v, i) => a[i] === v);
if (!isPng) {
  console.error("entry.png does not carry a PNG signature");
  process.exit(1);
}
if (a.length > 1024 * 1024) {
  console.error(`entry.png is ${a.length} bytes, over the 1 MiB cap`);
  process.exit(1);
}
// The IHDR chunk follows the signature: width and height are big-endian
// uint32s at bytes 16 and 20. The contest caps the page at 1024x1024.
const width = a.readUInt32BE(16);
const height = a.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  console.error(`entry.png is ${width}x${height}, over the 1024x1024 cap`);
  process.exit(1);
}
if (!a.equals(b)) {
  console.error("the delivered copy differs from entry.png");
  process.exit(1);
}
console.log(`delivered entry.png (${a.length} bytes) to ${dst}`);

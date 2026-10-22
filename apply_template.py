from pathlib import Path
from PIL import Image, ImageOps

input_dir = Path("./Photos")
output_dir = Path("./Output")
template_landscape_path = Path("./template_landscape.png")
template_portrait_path = Path("./template_portrait.png")

output_dir.mkdir(exist_ok=True)
valid_extensions = {".jpg", ".jpeg", ".png"}

for img_path in input_dir.iterdir():
    if img_path.suffix.lower() not in valid_extensions:
        continue

    with Image.open(img_path) as base_img:
        exif_data = base_img.info.get("exif")
        base_img = ImageOps.exif_transpose(base_img).convert("RGBA")
        width, height = base_img.size
        if height > width and template_portrait_path.exists():
            tpl_path = template_portrait_path
        else:
            tpl_path = template_landscape_path

        with Image.open(tpl_path) as tpl_img:
            tpl_resized = tpl_img.convert("RGBA").resize((width, height), Image.Resampling.LANCZOS)
            combined = Image.alpha_composite(base_img, tpl_resized).convert("RGB")

            out_file = output_dir / img_path.name
            if exif_data:
                combined.save(out_file, quality=100, subsampling=0, exif=exif_data)
            else:
                combined.save(out_file, quality=100, subsampling=0)

print("Batch processing complete.")
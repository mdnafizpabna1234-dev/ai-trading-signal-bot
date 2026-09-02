from PIL import Image
import io


def prepare_chart_image(image_bytes):
    """
    Prepare a trading chart screenshot for analysis.
    """

    image = Image.open(io.BytesIO(image_bytes))

    # Convert to RGB
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize large screenshots
    max_width = 1600

    if image.width > max_width:
        ratio = max_width / image.width
        new_height = int(image.height * ratio)
        image = image.resize((max_width, new_height))

    return image


def chart_image_received():
    return {
        "status": "ready",
        "message": "Chart screenshot is ready for AI analysis."
    }

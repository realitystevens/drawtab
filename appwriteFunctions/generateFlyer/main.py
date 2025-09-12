"""
Appwrite Function: Generate Flyer
"""
import json
import io
import base64
import requests
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Any, List, Tuple, Optional


def main(context):
    """
    Main function for generating flyers in Appwrite
    Expected payload:
    {
        "templateUrl": "https://...",
        "hotspots": [...],
        "data": {
            "text_hotspot_id": "John Doe",
            "image_hotspot_id": "https://..."
        }
    }
    """
    try:
        # Parse input
        payload = json.loads(context.req.body)
        template_url = payload.get('templateUrl')
        hotspots = payload.get('hotspots', [])
        data = payload.get('data', {})

        if not template_url:
            return context.res.json({
                'success': False,
                'error': 'Template URL is required'
            }, 400)

        # Generate flyer
        generator = AppwriteFlyerGenerator()
        result = generator.generate_flyer(template_url, hotspots, data)

        if result['success']:
            return context.res.json({
                'success': True,
                'data': {
                    'imageBase64': result['image_base64'],
                    'metadata': result['metadata']
                }
            })
        else:
            return context.res.json({
                'success': False,
                'error': result['error']
            }, 500)

    except Exception as e:
        return context.res.json({
            'success': False,
            'error': f'Function error: {str(e)}'
        }, 500)


class AppwriteFlyerGenerator:
    """
    Appwrite version of the Django FlyerGenerator
    """

    def __init__(self):
        self.default_font_size = 24
        self.default_font_color = '#000000'
        self.default_font_family = 'arial'

    def generate_flyer(self, template_url: str, hotspots: List[Dict], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a flyer with dynamic content
        """
        try:
            # Download template image
            template_image = self._download_image(template_url)
            if not template_image:
                return {'success': False, 'error': 'Failed to download template'}

            # Create a copy for editing
            flyer_image = template_image.copy()
            draw = ImageDraw.Draw(flyer_image)

            # Process each hotspot
            for hotspot in hotspots:
                hotspot_id = hotspot.get('id')
                hotspot_type = hotspot.get('type')

                if hotspot_id in data:
                    if hotspot_type == 'text':
                        self._add_text_to_hotspot(
                            draw, flyer_image, hotspot, data[hotspot_id])
                    elif hotspot_type == 'image':
                        self._add_image_to_hotspot(
                            flyer_image, hotspot, data[hotspot_id])

            # Convert to base64
            buffer = io.BytesIO()
            flyer_image.save(buffer, format='PNG', quality=95)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()

            return {
                'success': True,
                'image_base64': image_base64,
                'metadata': {
                    'width': flyer_image.width,
                    'height': flyer_image.height,
                    'format': 'PNG',
                    'hotspots_processed': len(hotspots)
                }
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _download_image(self, url: str) -> Optional[Image.Image]:
        """Download image from URL"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return Image.open(io.BytesIO(response.content))
        except Exception:
            return None

    def _add_text_to_hotspot(self, draw: ImageDraw.Draw, image: Image.Image, hotspot: Dict, text: str):
        """Add text to a hotspot area"""
        try:
            # Calculate position and size
            x = int((hotspot.get('x', 0) / 100) * image.width)
            y = int((hotspot.get('y', 0) / 100) * image.height)
            width = int((hotspot.get('width', 20) / 100) * image.width)
            height = int((hotspot.get('height', 10) / 100) * image.height)

            # Font settings
            font_size = hotspot.get('fontSize', self.default_font_size)
            font_color = hotspot.get('fontColor', self.default_font_color)
            text_align = hotspot.get('textAlign', 'left')

            # Try to load font (fallback to default if not available)
            try:
                font = ImageFont.truetype('arial.ttf', font_size)
            except:
                font = ImageFont.load_default()

            # Wrap text to fit width
            wrapped_text = self._wrap_text(text, font, width, draw)

            # Calculate text position based on alignment
            if text_align == 'center':
                text_x = x + (width // 2)
                anchor = 'mt'
            elif text_align == 'right':
                text_x = x + width
                anchor = 'rt'
            else:  # left
                text_x = x
                anchor = 'lt'

            # Draw text
            draw.text(
                (text_x, y),
                wrapped_text,
                font=font,
                fill=font_color,
                anchor=anchor
            )

        except Exception as e:
            print(f"Error adding text to hotspot: {e}")

    def _add_image_to_hotspot(self, base_image: Image.Image, hotspot: Dict, image_url: str):
        """Add image to a hotspot area"""
        try:
            # Download the image
            overlay_image = self._download_image(image_url)
            if not overlay_image:
                return

            # Calculate position and size
            x = int((hotspot.get('x', 0) / 100) * base_image.width)
            y = int((hotspot.get('y', 0) / 100) * base_image.height)
            width = int((hotspot.get('width', 20) / 100) * base_image.width)
            height = int((hotspot.get('height', 10) / 100) * base_image.height)

            # Resize and paste the image
            overlay_image = overlay_image.resize(
                (width, height), Image.Resampling.LANCZOS)

            # Convert to RGBA if needed for transparency
            if overlay_image.mode != 'RGBA':
                overlay_image = overlay_image.convert('RGBA')

            # Paste the image
            base_image.paste(overlay_image, (x, y), overlay_image)

        except Exception as e:
            print(f"Error adding image to hotspot: {e}")

    def _wrap_text(self, text: str, font: ImageFont.ImageFont, max_width: int, draw: ImageDraw.Draw) -> str:
        """Wrap text to fit within specified width"""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]

            if text_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Single word is too long, add it anyway
                    lines.append(word)

        if current_line:
            lines.append(' '.join(current_line))

        return '\n'.join(lines)


# Required for Appwrite function runtime
if __name__ == '__main__':
    # This will be called by Appwrite runtime
    pass

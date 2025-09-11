"""
Image processing utilities for flyer generation
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import logging
from typing import Dict, Any, Optional, Tuple
import math

logger = logging.getLogger(__name__)


class FlyerGenerator:
    """
    Main class for generating flyers from templates and dynamic data
    """

    def __init__(self):
        self.default_font_size = 24
        self.default_font_color = '#000000'
        self.font_cache = {}

    def generate_flyer(self, template_path: str, dynamic_areas: Dict[str, Any],
                       recipient_data: Dict[str, Any]) -> Optional[ContentFile]:
        """
        Generate a flyer by overlaying dynamic content on a template

        Args:
            template_path: Path to the template image
            dynamic_areas: Configuration for dynamic areas
            recipient_data: Data to fill into the template

        Returns:
            ContentFile with the generated flyer image
        """
        try:
            # Open the base template
            with default_storage.open(template_path, 'rb') as template_file:
                base_image = Image.open(template_file).convert('RGBA')

            # Create a copy to work with
            flyer_image = base_image.copy()

            # Process each dynamic area
            for area_config in dynamic_areas:
                self._process_dynamic_area(
                    flyer_image, area_config, recipient_data)

            # Convert to RGB for JPEG output
            if flyer_image.mode != 'RGB':
                # Create white background
                rgb_image = Image.new('RGB', flyer_image.size, (255, 255, 255))
                rgb_image.paste(flyer_image, mask=flyer_image.split(
                )[-1] if flyer_image.mode == 'RGBA' else None)
                flyer_image = rgb_image

            # Save to BytesIO
            output = io.BytesIO()
            flyer_image.save(output, format='JPEG', quality=95, optimize=True)
            output.seek(0)

            return ContentFile(output.getvalue(), name='generated_flyer.jpg')

        except Exception as e:
            logger.error(f"Error generating flyer: {str(e)}")
            return None

    def _process_dynamic_area(self, image: Image.Image, area_config: Dict[str, Any],
                              recipient_data: Dict[str, Any]) -> None:
        """
        Process a single dynamic area on the image
        """
        area_type = area_config.get('area_type')

        if area_type == 'photo':
            self._add_photo(image, area_config, recipient_data)
        elif area_type in ['name', 'message', 'date', 'custom_text']:
            self._add_text(image, area_config, recipient_data)

    def _add_photo(self, image: Image.Image, area_config: Dict[str, Any],
                   recipient_data: Dict[str, Any]) -> None:
        """
        Add a photo to the specified area
        """
        try:
            photo_path = recipient_data.get('photo_path')
            if not photo_path or not default_storage.exists(photo_path):
                return

            # Get area dimensions
            x = area_config.get('x_position', 0)
            y = area_config.get('y_position', 0)
            width = area_config.get('width', 100)
            height = area_config.get('height', 100)

            # Load and resize photo
            with default_storage.open(photo_path, 'rb') as photo_file:
                photo = Image.open(photo_file).convert('RGBA')

            # Resize photo to fit area while maintaining aspect ratio
            photo = self._resize_image_to_fit(photo, (width, height))

            # Apply styling
            border_radius = area_config.get('border_radius', 0)
            if border_radius > 0:
                photo = self._apply_rounded_corners(photo, border_radius)

            border_width = area_config.get('border_width', 0)
            border_color = area_config.get('border_color', '#000000')
            if border_width > 0:
                photo = self._apply_border(photo, border_width, border_color)

            # Center the photo in the area
            photo_x = x + (width - photo.width) // 2
            photo_y = y + (height - photo.height) // 2

            # Paste photo onto main image
            if photo.mode == 'RGBA':
                image.paste(photo, (photo_x, photo_y), photo)
            else:
                image.paste(photo, (photo_x, photo_y))

        except Exception as e:
            logger.error(f"Error adding photo: {str(e)}")

    def _add_text(self, image: Image.Image, area_config: Dict[str, Any],
                  recipient_data: Dict[str, Any]) -> None:
        """
        Add text to the specified area
        """
        try:
            # Get text content based on area type
            text_content = self._get_text_content(area_config, recipient_data)
            if not text_content:
                return

            # Get area configuration
            x = area_config.get('x_position', 0)
            y = area_config.get('y_position', 0)
            width = area_config.get('width', 200)
            height = area_config.get('height', 50)

            # Font configuration
            font_family = area_config.get('font_family', 'Arial')
            font_size = area_config.get('font_size', self.default_font_size)
            font_color = area_config.get('font_color', self.default_font_color)
            font_weight = area_config.get('font_weight', 'normal')
            text_align = area_config.get('text_align', 'center')

            # Load font
            font = self._get_font(font_family, font_size, font_weight)

            # Create drawing context
            draw = ImageDraw.Draw(image)

            # Handle text wrapping and sizing
            wrapped_text, final_font = self._fit_text_to_area(
                text_content, font, width, height, draw
            )

            # Calculate text position based on alignment
            text_x, text_y = self._calculate_text_position(
                wrapped_text, final_font, x, y, width, height, text_align, draw
            )

            # Convert color to RGB tuple
            rgb_color = self._hex_to_rgb(font_color)

            # Draw text
            draw.multiline_text(
                (text_x, text_y),
                wrapped_text,
                font=final_font,
                fill=rgb_color,
                align=text_align,
                spacing=4
            )

        except Exception as e:
            logger.error(f"Error adding text: {str(e)}")

    def _get_text_content(self, area_config: Dict[str, Any],
                          recipient_data: Dict[str, Any]) -> str:
        """
        Get the text content for a text area based on its type
        """
        area_type = area_config.get('area_type')

        if area_type == 'name':
            first_name = recipient_data.get('first_name', '')
            last_name = recipient_data.get('last_name', '')
            return f"{first_name} {last_name}".strip()

        elif area_type == 'message':
            return recipient_data.get('custom_message', area_config.get('default_text', ''))

        elif area_type == 'date':
            event_date = recipient_data.get('event_date')
            if event_date:
                return event_date.strftime('%B %d, %Y')
            return ''

        elif area_type == 'custom_text':
            return recipient_data.get(area_config.get('data_key', ''), area_config.get('default_text', ''))

        return ''

    def _get_font(self, font_family: str, font_size: int, font_weight: str) -> ImageFont.ImageFont:
        """
        Get or load a font with caching
        """
        font_key = f"{font_family}_{font_size}_{font_weight}"

        if font_key in self.font_cache:
            return self.font_cache[font_key]

        try:
            # Try to load system font
            if font_weight == 'bold':
                font_path = self._get_system_font_path(font_family, bold=True)
            else:
                font_path = self._get_system_font_path(font_family, bold=False)

            if font_path and os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
            else:
                # Fallback to default font
                font = ImageFont.load_default()

        except Exception:
            # Ultimate fallback
            font = ImageFont.load_default()

        self.font_cache[font_key] = font
        return font

    def _get_system_font_path(self, font_family: str, bold: bool = False) -> Optional[str]:
        """
        Get system font path for common fonts
        """
        font_map = {
            'Arial': 'arial.ttf' if not bold else 'arialbd.ttf',
            'Helvetica': 'arial.ttf' if not bold else 'arialbd.ttf',  # Fallback to Arial
            'Times New Roman': 'times.ttf' if not bold else 'timesbd.ttf',
            'Georgia': 'georgia.ttf' if not bold else 'georgiab.ttf',
            'Verdana': 'verdana.ttf' if not bold else 'verdanab.ttf',
            'Trebuchet MS': 'trebuc.ttf' if not bold else 'trebucbd.ttf',
            'Impact': 'impact.ttf',
            'Comic Sans MS': 'comic.ttf' if not bold else 'comicbd.ttf',
        }

        font_file = font_map.get(font_family, 'arial.ttf')

        # Windows font paths
        windows_path = f"C:/Windows/Fonts/{font_file}"
        if os.path.exists(windows_path):
            return windows_path

        # Linux font paths
        linux_paths = [
            f"/usr/share/fonts/truetype/dejavu/{font_file}",
            f"/usr/share/fonts/truetype/liberation/{font_file}",
            f"/System/Library/Fonts/{font_file}",  # macOS
        ]

        for path in linux_paths:
            if os.path.exists(path):
                return path

        return None

    def _fit_text_to_area(self, text: str, font: ImageFont.ImageFont,
                          max_width: int, max_height: int,
                          draw: ImageDraw.ImageDraw) -> Tuple[str, ImageFont.ImageFont]:
        """
        Fit text to the specified area by adjusting font size and wrapping
        """
        original_font = font
        current_font = font

        # Try reducing font size if text doesn't fit
        for font_size_reduction in range(0, 10):
            if font_size_reduction > 0:
                try:
                    new_size = max(8, font.size - font_size_reduction * 2)
                    if hasattr(font, 'path'):
                        current_font = ImageFont.truetype(font.path, new_size)
                    else:
                        current_font = ImageFont.load_default()
                except:
                    current_font = ImageFont.load_default()

            # Try wrapping text
            wrapped_text = self._wrap_text(text, current_font, max_width, draw)

            # Check if it fits
            text_bbox = draw.multiline_textbbox(
                (0, 0), wrapped_text, font=current_font)
            text_height = text_bbox[3] - text_bbox[1]

            if text_height <= max_height:
                return wrapped_text, current_font

        # If still doesn't fit, truncate
        lines = wrapped_text.split('\n')
        while len(lines) > 1:
            lines = lines[:-1]
            test_text = '\n'.join(lines) + '...'
            text_bbox = draw.multiline_textbbox(
                (0, 0), test_text, font=current_font)
            text_height = text_bbox[3] - text_bbox[1]
            if text_height <= max_height:
                return test_text, current_font

        return lines[0] if lines else '', current_font

    def _wrap_text(self, text: str, font: ImageFont.ImageFont,
                   max_width: int, draw: ImageDraw.ImageDraw) -> str:
        """
        Wrap text to fit within the specified width
        """
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            text_bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = text_bbox[2] - text_bbox[0]

            if text_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Word is too long, break it
                    lines.append(word)

        if current_line:
            lines.append(' '.join(current_line))

        return '\n'.join(lines)

    def _calculate_text_position(self, text: str, font: ImageFont.ImageFont,
                                 x: int, y: int, width: int, height: int,
                                 align: str, draw: ImageDraw.ImageDraw) -> Tuple[int, int]:
        """
        Calculate text position based on alignment
        """
        text_bbox = draw.multiline_textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Horizontal alignment
        if align == 'center':
            text_x = x + (width - text_width) // 2
        elif align == 'right':
            text_x = x + width - text_width
        else:  # left
            text_x = x

        # Vertical alignment (always center)
        text_y = y + (height - text_height) // 2

        return text_x, text_y

    def _resize_image_to_fit(self, image: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
        """
        Resize image to fit within target size while maintaining aspect ratio
        """
        target_width, target_height = target_size
        img_width, img_height = image.size

        # Calculate scaling factor
        scale_x = target_width / img_width
        scale_y = target_height / img_height
        scale = min(scale_x, scale_y)

        # Calculate new size
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def _apply_rounded_corners(self, image: Image.Image, radius: int) -> Image.Image:
        """
        Apply rounded corners to an image
        """
        # Create mask
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)

        # Apply mask
        output = Image.new('RGBA', image.size, (0, 0, 0, 0))
        output.paste(image, (0, 0))
        output.putalpha(mask)

        return output

    def _apply_border(self, image: Image.Image, border_width: int, border_color: str) -> Image.Image:
        """
        Apply border to an image
        """
        # Create new image with border
        new_size = (image.width + 2 * border_width,
                    image.height + 2 * border_width)
        bordered_image = Image.new(
            'RGBA', new_size, self._hex_to_rgb(border_color) + (255,))

        # Paste original image in center
        bordered_image.paste(image, (border_width, border_width),
                             image if image.mode == 'RGBA' else None)

        return bordered_image

    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """
        Convert hex color to RGB tuple
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


# Utility functions

def validate_template_image(image_file) -> Dict[str, Any]:
    """
    Validate and get information about uploaded template image
    """
    try:
        with Image.open(image_file) as img:
            return {
                'valid': True,
                'width': img.width,
                'height': img.height,
                'format': img.format,
                'mode': img.mode,
                'size_mb': len(image_file.read()) / (1024 * 1024)
            }
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }


def create_template_thumbnail(image_file, thumbnail_size: Tuple[int, int] = (300, 300)) -> Optional[ContentFile]:
    """
    Create a thumbnail for a template image
    """
    try:
        with Image.open(image_file) as img:
            img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)

            output = io.BytesIO()
            img.save(output, format='JPEG', quality=85)
            output.seek(0)

            return ContentFile(output.getvalue(), name='thumbnail.jpg')
    except Exception as e:
        logger.error(f"Error creating thumbnail: {str(e)}")
        return None

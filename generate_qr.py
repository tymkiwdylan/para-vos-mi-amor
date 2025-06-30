#!/usr/bin/env python3
"""
Romantic QR Code Generator for Para vos, mi amor 💕
Generates a beautiful QR code with heart border and romantic styling
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os

def create_heart_border(draw, center_x, center_y, size, color, thickness=5):
    """Draw a heart shape border around the QR code"""
    scale = size / 200  # Scale factor based on desired size
    
    # Heart equation: (x²+y²-1)³-x²y³=0
    # We'll approximate with curves for better visual effect
    points = []
    
    for angle in range(0, 360, 2):
        t = math.radians(angle)
        # Parametric heart equations
        x = 16 * math.sin(t)**3
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        
        # Scale and translate
        heart_x = center_x + x * scale * 0.8
        heart_y = center_y - y * scale * 0.8  # Negative because PIL y-axis is flipped
        
        points.append((heart_x, heart_y))
    
    # Draw the heart outline with multiple strokes for thickness
    for i in range(thickness):
        offset_points = []
        for x, y in points:
            offset_points.append((x + i/2, y + i/2))
        
        if len(offset_points) > 2:
            draw.polygon(offset_points, outline=color, fill=None, width=2)

def create_gradient_background(size, color1, color2):
    """Create a beautiful gradient background"""
    gradient = Image.new('RGB', size, color1)
    draw = ImageDraw.Draw(gradient)
    
    for i in range(size[1]):
        # Interpolate between colors
        ratio = i / size[1]
        r1, g1, b1 = tuple(int(color1[j:j+2], 16) for j in (1, 3, 5))
        r2, g2, b2 = tuple(int(color2[j:j+2], 16) for j in (1, 3, 5))
        
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        
        draw.line([(0, i), (size[0], i)], fill=(r, g, b))
    
    return gradient

def add_sparkles(draw, canvas_size, count=20):
    """Add sparkle effects around the design"""
    import random
    
    sparkle_positions = []
    for _ in range(count):
        x = random.randint(50, canvas_size[0] - 50)
        y = random.randint(50, canvas_size[1] - 50)
        sparkle_positions.append((x, y))
    
    for x, y in sparkle_positions:
        # Draw a star-like sparkle
        size = random.randint(8, 15)
        color = random.choice(["#ffd700", "#ff6b9d", "#ffffff", "#ffa4c4"])
        
        # Draw sparkle as a plus sign with diagonal lines
        draw.line([(x-size, y), (x+size, y)], fill=color, width=2)
        draw.line([(x, y-size), (x, y+size)], fill=color, width=2)
        draw.line([(x-size//2, y-size//2), (x+size//2, y+size//2)], fill=color, width=1)
        draw.line([(x-size//2, y+size//2), (x+size//2, y-size//2)], fill=color, width=1)

def create_romantic_qr():
    """Create a beautiful romantic QR code with heart border"""
    
    # Your love card URL
    url = "http://tymkiwdylan.github.io/para-vos-mi-amor/"
    
    # Create QR code with high quality settings
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=18,  # Slightly smaller to fit in heart
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image with romantic colors
    qr_img = qr.make_image(
        fill_color="#ff6b9d",
        back_color="#fff8f0"
    )
    
    qr_img = qr_img.convert('RGB')
    
    # Create gradient background
    canvas_size = (900, 1000)
    canvas = create_gradient_background(canvas_size, "#fff8f0", "#ffeef0")
    
    # Calculate positions
    qr_size = qr_img.size
    qr_center_x = canvas_size[0] // 2
    qr_center_y = (canvas_size[1] // 2) - 20
    qr_position = (
        qr_center_x - qr_size[0] // 2,
        qr_center_y - qr_size[1] // 2
    )
    
    # Create a soft shadow effect for the QR code
    shadow_img = Image.new('RGBA', (qr_size[0] + 20, qr_size[1] + 20), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    shadow_draw.rectangle([10, 10, qr_size[0] + 10, qr_size[1] + 10], 
                         fill=(0, 0, 0, 50))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=5))
    
    # Paste shadow first
    canvas.paste(shadow_img, 
                (qr_position[0] - 10, qr_position[1] - 10), 
                shadow_img)
    
    # Paste QR code
    canvas.paste(qr_img, qr_position)
    
    # Draw decorative elements
    draw = ImageDraw.Draw(canvas)
    
    # Create beautiful heart border around QR code
    heart_size = max(qr_size) + 100
    create_heart_border(draw, qr_center_x, qr_center_y, heart_size, "#ff6b9d", thickness=8)
    
    # Add inner heart border with different color
    create_heart_border(draw, qr_center_x, qr_center_y, heart_size - 20, "#ffd700", thickness=4)
    
    # Add sparkles around the design
    add_sparkles(draw, canvas_size, count=25)
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("Arial", 42)
        subtitle_font = ImageFont.truetype("Arial", 28)
        url_font = ImageFont.truetype("Arial", 20)
        heart_font = ImageFont.truetype("Arial", 50)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        url_font = ImageFont.load_default()
        heart_font = ImageFont.load_default()
    
    # Add title with shadow effect
    title_text = "💕 Para vos, mi amor 💕"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (canvas_size[0] - title_width) // 2
    title_y = 60
    
    # Draw text shadow
    draw.text((title_x + 2, title_y + 2), title_text, fill="#764ba2", font=title_font)
    # Draw main text
    draw.text((title_x, title_y), title_text, fill="#ff6b9d", font=title_font)
    
    # Add subtitle
    subtitle_text = "Escanea para ver mi mensaje de amor"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (canvas_size[0] - subtitle_width) // 2
    subtitle_y = qr_position[1] + qr_size[1] + 80
    
    # Subtitle with shadow
    draw.text((subtitle_x + 1, subtitle_y + 1), subtitle_text, fill="#9a7fb8", font=subtitle_font)
    draw.text((subtitle_x, subtitle_y), subtitle_text, fill="#764ba2", font=subtitle_font)
    
    # Add URL
    url_text = "tymkiwdylan.github.io/para-vos-mi-amor"
    url_bbox = draw.textbbox((0, 0), url_text, font=url_font)
    url_width = url_bbox[2] - url_bbox[0]
    url_x = (canvas_size[0] - url_width) // 2
    url_y = subtitle_y + 50
    
    # URL with shadow
    draw.text((url_x + 1, url_y + 1), url_text, fill="#e6c200", font=url_font)
    draw.text((url_x, url_y), url_text, fill="#ffd700", font=url_font)
    
    # Add decorative corner hearts with gradient effect
    corner_hearts = ["💕", "💖", "💝", "💗"]
    positions = [(80, 80), (canvas_size[0] - 120, 80), 
                (80, canvas_size[1] - 120), (canvas_size[0] - 120, canvas_size[1] - 120)]
    
    for i, (x, y) in enumerate(positions):
        heart = corner_hearts[i % len(corner_hearts)]
        # Shadow
        draw.text((x + 2, y + 2), heart, fill="#cc5577", font=heart_font)
        # Main heart
        draw.text((x, y), heart, fill="#ff6b9d", font=heart_font)
    
    # Add decorative border around entire image
    border_thickness = 8
    for i in range(border_thickness):
        draw.rectangle([i, i, canvas_size[0] - i - 1, canvas_size[1] - i - 1], 
                      outline="#ff6b9d", width=1)
    
    # Add inner decorative border
    inner_border = 20
    for i in range(3):
        draw.rectangle([inner_border + i, inner_border + i, 
                       canvas_size[0] - inner_border - i - 1, 
                       canvas_size[1] - inner_border - i - 1], 
                      outline="#ffd700", width=1)
    
    return canvas

def create_high_res_qr():
    """Create a high-resolution version perfect for printing"""
    url = "http://tymkiwdylan.github.io/para-vos-mi-amor/"
    
    # Higher resolution settings for printing
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=35,
        border=8,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    qr_img = qr.make_image(
        fill_color="#ff6b9d",
        back_color="#fff8f0"
    )
    
    qr_img = qr_img.convert('RGB')
    
    # Larger canvas for print quality
    canvas_size = (1800, 2000)
    canvas = create_gradient_background(canvas_size, "#fff8f0", "#ffeef0")
    
    qr_size = qr_img.size
    qr_center_x = canvas_size[0] // 2
    qr_center_y = (canvas_size[1] // 2) - 40
    qr_position = (
        qr_center_x - qr_size[0] // 2,
        qr_center_y - qr_size[1] // 2
    )
    
    # Create shadow effect
    shadow_img = Image.new('RGBA', (qr_size[0] + 40, qr_size[1] + 40), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    shadow_draw.rectangle([20, 20, qr_size[0] + 20, qr_size[1] + 20], 
                         fill=(0, 0, 0, 50))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=10))
    
    canvas.paste(shadow_img, 
                (qr_position[0] - 20, qr_position[1] - 20), 
                shadow_img)
    canvas.paste(qr_img, qr_position)
    
    draw = ImageDraw.Draw(canvas)
    
    # Create heart border (scaled up)
    heart_size = max(qr_size) + 200
    create_heart_border(draw, qr_center_x, qr_center_y, heart_size, "#ff6b9d", thickness=16)
    create_heart_border(draw, qr_center_x, qr_center_y, heart_size - 40, "#ffd700", thickness=8)
    
    # Add sparkles (more for print version)
    add_sparkles(draw, canvas_size, count=50)
    
    # High resolution fonts
    try:
        title_font = ImageFont.truetype("Arial", 84)
        subtitle_font = ImageFont.truetype("Arial", 56)
        url_font = ImageFont.truetype("Arial", 40)
        heart_font = ImageFont.truetype("Arial", 100)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        url_font = ImageFont.load_default()
        heart_font = ImageFont.load_default()
    
    # Add all text elements with shadows (scaled up)
    title_text = "💕 Para vos, mi amor 💕"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (canvas_size[0] - title_width) // 2
    title_y = 120
    
    draw.text((title_x + 4, title_y + 4), title_text, fill="#764ba2", font=title_font)
    draw.text((title_x, title_y), title_text, fill="#ff6b9d", font=title_font)
    
    subtitle_text = "Escanea para ver mi mensaje de amor"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (canvas_size[0] - subtitle_width) // 2
    subtitle_y = qr_position[1] + qr_size[1] + 160
    
    draw.text((subtitle_x + 2, subtitle_y + 2), subtitle_text, fill="#9a7fb8", font=subtitle_font)
    draw.text((subtitle_x, subtitle_y), subtitle_text, fill="#764ba2", font=subtitle_font)
    
    url_text = "tymkiwdylan.github.io/para-vos-mi-amor"
    url_bbox = draw.textbbox((0, 0), url_text, font=url_font)
    url_width = url_bbox[2] - url_bbox[0]
    url_x = (canvas_size[0] - url_width) // 2
    url_y = subtitle_y + 100
    
    draw.text((url_x + 2, url_y + 2), url_text, fill="#e6c200", font=url_font)
    draw.text((url_x, url_y), url_text, fill="#ffd700", font=url_font)
    
    # Corner hearts (scaled up)
    corner_hearts = ["💕", "💖", "💝", "💗"]
    positions = [(160, 160), (canvas_size[0] - 240, 160), 
                (160, canvas_size[1] - 240), (canvas_size[0] - 240, canvas_size[1] - 240)]
    
    for i, (x, y) in enumerate(positions):
        heart = corner_hearts[i % len(corner_hearts)]
        draw.text((x + 4, y + 4), heart, fill="#cc5577", font=heart_font)
        draw.text((x, y), heart, fill="#ff6b9d", font=heart_font)
    
    # Decorative borders (scaled up)
    border_thickness = 16
    for i in range(border_thickness):
        draw.rectangle([i, i, canvas_size[0] - i - 1, canvas_size[1] - i - 1], 
                      outline="#ff6b9d", width=2)
    
    inner_border = 40
    for i in range(6):
        draw.rectangle([inner_border + i, inner_border + i, 
                       canvas_size[0] - inner_border - i - 1, 
                       canvas_size[1] - inner_border - i - 1], 
                      outline="#ffd700", width=2)
    
    return canvas

def main():
    """Generate and save the romantic QR code"""
    print("🎨 Generating your beautifully styled romantic QR code...")
    
    try:
        qr_image = create_romantic_qr()
        
        # Save the image
        output_path = "romantic_qr_code.png"
        qr_image.save(output_path, "PNG", quality=95, optimize=True)
        
        print(f"✨ Beautiful QR code with heart border saved as '{output_path}'")
        print("💕 Perfect for printing and sharing your love!")
        print(f"📱 Points to: http://tymkiwdylan.github.io/para-vos-mi-amor/")
        
        # Also create a high-resolution version for printing
        hr_output_path = "romantic_qr_code_print.png"
        hr_qr_image = create_high_res_qr()
        hr_qr_image.save(hr_output_path, "PNG", quality=100, optimize=True)
        print(f"🖨️  High-resolution print version saved as '{hr_output_path}'")
        print("🌟 Features: Heart border, gradient background, sparkles, and shadows!")
        
    except Exception as e:
        print(f"❌ Error generating QR code: {e}")
        print("💡 Make sure you have 'qrcode' and 'pillow' installed:")
        print("   pip install qrcode[pil] pillow")

if __name__ == "__main__":
    main() 
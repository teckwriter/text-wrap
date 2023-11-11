from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_text_box(text, canvas_width, canvas_height, max_width, text_align, box_align,
                    font_path, font_size=12, font_color="black", 
                    background_color="white", line_spacing=0, padding=10
                    ):
    # Create a blank canvas with a white background
    canvas = Image.new("RGB", (canvas_width, canvas_height), background_color)
    draw = ImageDraw.Draw(canvas)
    
    # Load the font and set the font size
    if font_path is None:
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(font_path, font_size)

    # Split the text into lines that fit within the canvas
    wrapper = textwrap.TextWrapper(width=max_width * 1.6 // font_size)  # Adjust the width as needed
    lines = wrapper.wrap(text)

    # Calculate the total height needed for the text with line spacing and padding
    total_height = 0
    max_line_width = 0  # Track the maximum line width within the text
    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        total_height += text_bbox[3] - text_bbox[1] + line_spacing
        max_line_width = max(max_line_width, text_bbox[2] - text_bbox[0])
    
    # Calculate the bounding box width based on max_width or the maximum line width
    bounding_box_width = min(max_width, max_line_width)
    
    # Calculate the X-coordinate to align the text horizontally
    if box_align == "left":
        x = padding * 5  # Align to the left with padding
    elif box_align == "right":
        x = canvas_width - bounding_box_width - padding * 5  # Align to the right with padding
    else:
        x = (canvas_width - bounding_box_width) // 2  # Center align
    
    # Calculate the Y-coordinate to vertically center the text
    y = (canvas_height - total_height) // 2
    
    # Draw the bounding box around the text
    draw.rectangle(
        [x - padding, y - padding, x + bounding_box_width + padding, y + total_height + padding],
        outline="red"
    )
    
    # Reset y for drawing the text
    y = (canvas_height - total_height) // 2
    
    # Draw the text within the bounding box with line spacing
    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        # Calculate x-coordinate based on alignment
        if text_align == "left":
            text_x = x  # Align text to the left within the bounding box
        elif text_align == "right":
            text_x = x + bounding_box_width - (text_bbox[2] - text_bbox[0])  # Align text to the right within the bounding box
        else:
            text_x = x + (bounding_box_width - (text_bbox[2] - text_bbox[0])) // 2  # Center align text within the bounding box
        draw.text((text_x, y), line , fill=font_color, font=font)
        y += text_bbox[3] - text_bbox[1] + line_spacing
    # Save the canvas as an image
    canvas.save(fr'Bounding_Box\alignments_testcase\{box_align}-{text_align}.png')
    # Show the canvas
    canvas.show()

# Example usage with different alignments
text = "Hi, welcome to the bounding box concept. How is it going? This is about text wrapping tool. The text will go to the next Line."
canvas_width = 1080  # Adjust the canvas width as needed
canvas_height = 1080  # Adjust the canvas height as needed
font_path = r"c:\WINDOWS\Fonts\TIMESBD.TTF"  # Replace with the path to your desired font file
font_size = 50
font_color = "black"
background_color = "whitesmoke"
max_width = 600
line_spacing = 20  # Adjust the line spacing as needed
padding = 10  # Adjust the padding as needed
box_align = "center" # Adjust the box alignment as needed ["center", "right", "left"]
text_align = "left"  # Adjust the text alignment as needed ["center", "right", "left"]

# Create text boxes with different alignments
create_text_box(text, canvas_width, canvas_height, max_width, text_align, box_align,
                font_path, font_size, font_color, background_color, 
                line_spacing, padding)
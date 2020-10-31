from PIL import Image 

# Open image 
im = Image.open('cogai.jpg')

# Make transform matrix, to multiply R by 1.5, leaving G and B unchanged
Matrix = ( 1.5, 0,  0, 0, 
           0,   1,  0, 0, 
           0,   0,  1, 0) 

# Apply transform and save 
im = im.convert("RGB", Matrix) 
im.save('result.png') 
#!/bin/bash

file=$1
filename=$file
output="out.PNG"


#echo "Image $filename processing..."

#echo "Cropping image..."
convert $filename +repage -crop 28x18+585+400 $output
filename="in.PNG"
mv $output $filename
#display $filename
#echo "Image Cropped"

#echo "Resizing  image..."
convert $filename -resize 300x380 $output
mv $output $filename
#display $filename
#echo "Image resized"

#echo "Contrast  $filename ..."
convert $filename -sigmoidal-contrast 20 $output 
mv $output $filename
#display $filename 
#echo "Image Contrast"

convert $filename -threshold 50% $output
mv $output $filename
#display $filename
#echo "Sharpen $filename ..."
convert $filename -sharpen 0x2 $output 
mv $output $filename
#display $filename 
#echo "Image Sharpened"


#echo "Extract objects..."
python extract.py $filename $output> /dev/null 
mv $output $filename
rm ./edges.png
rm ./rejected.png
rm ./processed.png
#display $filename 
#echo "Objects Extraced"


#echo "Analyze objects..."
tesseract $filename output 1>/dev/null 2>&1
cat output.txt | grep -o '[0-9]*'
rm ./output.txt
rm ./in.PNG

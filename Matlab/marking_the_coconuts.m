image = imread('coconut.png');
image2 = imread('coconut.png');
image3 = ones(10000,10000);
imwrite(image3, 'white.png');
image3 = imread('white.png');
hold on

% Load annotations
A = csvread('annotations/selected_coconuts.csv');
y1_ann = A(:,1);
x1_ann = A(:,2);

B = csvread('annotations/selected_background.csv');
y2_ann = B(:,1);
x2_ann = B(:,2);

%Number of annotations
nr1_ann = size(x1_ann, 1);
nr2_ann = size(x2_ann, 1);

%Draw rectangles according to annotations
for i=1:nr1_ann
    x_top= x1_ann(i)-50;
    y_top = y1_ann(i)-50;   
    image = insertShape(image, 'FilledRectangle', [x_top y_top 100 100], 'Color', uint8([0 0 0]), 'Opacity', 1.0);
    image2 = insertShape(image2, 'FilledRectangle', [x_top y_top 100 100], 'Color', 'black', 'Opacity', 0.5);
    image3 = insertShape(image3, 'FilledRectangle', [x_top y_top 100 100], 'Color', uint8([0 0 0]), 'Opacity', 1.0);
end

for i=1:nr2_ann
    x_top= x2_ann(i)-50;
    y_top = y2_ann(i)-50;  
    image = insertShape(image, 'FilledRectangle', [x_top y_top 100 100], 'Color', uint8([0 0 0]), 'Opacity', 1.0);
    image2 = insertShape(image2, 'FilledRectangle', [x_top y_top 100 100], 'Color', 'blue', 'Opacity', 0.5);
    image3 = insertShape(image3, 'FilledRectangle', [x_top y_top 100 100], 'Color', uint8([0 0 0]), 'Opacity', 1.0);
end

imwrite(image, 'marked_black_coconuts_background.png');
imwrite(image2, 'marked_color_coconuts_background.png');
imwrite(image3, 'marked_black_white_coconuts_background.png');

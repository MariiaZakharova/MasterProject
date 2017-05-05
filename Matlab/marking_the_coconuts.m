image = imread('coconut.png');
image2 = imread('coconut.png');

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

% +1 because in Matlab indexes begin from 1, not from 0
    top_left_x = x1_ann(i) - 50 + 1;
    top_left_y = y1_ann(i) - 50 + 1;  
    image = insertShape(image, 'FilledRectangle', [top_left_x top_left_y 100 100], 'Color', uint8([0 0 0]), 'Opacity', 1.0);
    image2 = insertShape(image2, 'FilledRectangle', [top_left_x top_left_y 100 100], 'Color', 'black', 'Opacity', 0.5);

end

for i=1:nr2_ann
    top_left_x = x2_ann(i) - 50 + 1;
    top_left_y = y2_ann(i) - 50 + 1;  
    image = insertShape(image, 'FilledRectangle', [top_left_x top_left_y 100 100], 'Color', uint8([0 0 0]), 'Opacity', 1.0);
    image2 = insertShape(image2, 'FilledRectangle', [top_left_x top_left_y 100 100], 'Color', 'blue', 'Opacity', 0.5);
end

imwrite(image, 'marked_black_coconuts_background2.png');
imwrite(image2, 'marked_color_coconuts_background2.png');

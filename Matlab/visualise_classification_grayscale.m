image = imread('marked_black_white_coconuts_background.png');
hold on

% Load annotations
A = csvread('annotations/classification_all.csv');
y_ann = A(:,1);
x_ann = A(:,2);
z_ann = A(:,3);

%Number of annotations
nr_ann = size(x_ann, 1);

%Draw rectangles according to annotations
for i=1:nr_ann
    x_top= x_ann(i)-50;
    y_top = y_ann(i)-50; 
    z = z_ann(i);
    image = insertShape(image, 'FilledRectangle', [x_top y_top 100 100], 'Color', 'black', 'Opacity', z); 
end

imwrite(image, 'classification_black_white2.png');
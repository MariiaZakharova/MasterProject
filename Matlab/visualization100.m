image = ones(10000,10000);
imwrite(image, 'white.png');

image = imread('white.png');
hold on

% Load annotations
A = csvread('annotations/coords.csv');
y_ann = A(:,1);
x_ann = A(:,2);

%Number of annotations
nr_ann = size(x_ann, 1);

%Draw rectangles according to annotations
for i=1:nr_ann
    x_top= x_ann(i)-50;
    y_top = y_ann(i)-50;   
    image = insertShape(image, 'FilledRectangle', [x_top y_top 100 100], 'Color', 'black', 'Opacity', 1.0); 
end

imwrite(image, 'annotation_black_white2.png');

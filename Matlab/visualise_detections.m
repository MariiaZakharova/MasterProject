% Draw detections for specific threshold

% Threshold for P = 89%, R = 89%
%thresh = 108.8;
thresh = 1;

detections = csvread('detection_files/coconut_model1.txt');

% Remove detections below threshold
indices = detections(:,6) >= thresh;
detections = detections(indices, :);

% Load image
image = imread('marked_color_coconuts_background.png');
%figure(1);
%imshow(image);
hold on

% Load annotations
A = csvread('annotations/leftover_coconuts.csv');
y_ann = A(:,1);
x_ann = A(:,2);

% Remove annotations in top part
%indices = (y_ann > 5050);
% Remove annotations in bottom part (black area)
indices2 = (y_ann < 9760);
%final_indices = and(indices, indices2);
y_ann = y_ann(indices2);
x_ann = x_ann(indices2);
nr_ann = size(x_ann, 1);

% Shift annotations upwards
%y_ann = y_ann - 5000;

% Set in correct format
ann_ref = [x_ann-50 y_ann-50 ones(nr_ann,1)*100 ones(nr_ann,1)*100];

% Reform dets
dets_ref = detections(:,2:5);

[TP, FP, FN, bb_tp, bb_fp, bb_fn] = calc_type(ann_ref, dets_ref, 0.5);

%% Plot TP

for i=1:size(bb_tp,1)
    x_top= bb_tp(i,1);
    y_top = bb_tp(i,2);
    x_bottom = x_top + 100;
    y_bottom = y_top + 100;
    %line([x_top x_bottom x_bottom x_top x_top],[y_top y_top y_bottom y_bottom y_top],'linewidth', 1,'color','g');   
    %image = insertShape(image, 'rectangle', [x_top y_top 100 100], 'color', 'g', 'opacity', 0.6);
    %image = insertShape(image, 'FilledRectangle', [x_top-1 y_top-1 102 102], 'color', 'g', 'opacity', 0.3); 
    image = insertShape(image, 'FilledRectangle', [x_top y_top 100 100], 'color', 'g', 'opacity', 0.3);
    i
    size(bb_tp,1)
end


%% Plot FP

for i=1:size(bb_fp,1)
    x_top= bb_fp(i,1);
    y_top = bb_fp(i,2);
    x_bottom = x_top + 100;
    y_bottom = y_top + 100;
    %line([x_top x_bottom x_bottom x_top x_top],[y_top y_top y_bottom y_bottom y_top],'linewidth', 1,'color','r');   
    %image = insertShape(image, 'rectangle', [x_top y_top 100 100], 'color', 'r', 'opacity', 0.6);
    %image = insertShape(image, 'FilledRectangle', [x_top-1 y_top-1 102 102], 'color', 'r', 'opacity', 0.3); 
    image = insertShape(image, 'FilledRectangle', [x_top y_top 100 100], 'color', 'r', 'opacity', 0.3);
    i
    size(bb_fp,1)
end


%% Plot FN

for i=1:size(bb_fn,1)
    x_top= bb_fn(i,1);
    y_top = bb_fn(i,2);
    x_bottom = x_top + 100;
    y_bottom = y_top + 100;
    %line([x_top x_bottom x_bottom x_top x_top],[y_top y_top y_bottom y_bottom y_top],'linewidth', 1,'color','m');   
    %image = insertShape(image, 'rectangle', [x_top y_top 100 100], 'color', 'm', 'opacity', 0.6);
    %image = insertShape(image, 'FilledRectangle', [x_top-1 y_top-1 102 102], 'color', 'm', 'opacity', 0.3);
    image = insertShape(image, 'FilledRectangle', [x_top y_top 100 100], 'color', 'm', 'opacity', 0.3);
    i
    size(bb_fn,1)
end

imwrite(image, 'output_detections.png');




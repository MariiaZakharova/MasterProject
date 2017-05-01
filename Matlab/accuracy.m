% Calculate the detection accuracy
% Load annotations;
A = csvread('annotations/leftover_coconuts.csv');

% Load detections
model_name = 'coconut_model1';

detections = csvread(['detection_files/' model_name '.txt']);

% Define needed overlap
overlap = 0.5;

y_ann = A(:,1);
x_ann = A(:,2);

% Remove annotations in specific parts

% Remove annotations in top part
%indices = (y_ann > 5050);

% Remove annotations in bottom part (black area)
indices2 = (y_ann < 9760);

%final_indices = and(indices, indices2);
y_ann = y_ann(indices2);
x_ann = x_ann(indices2);

% Shift annotations upwards
%y_ann = y_ann - 5000;

% Set in correct format
nr_ann = size(x_ann, 1);
ann = [x_ann-50 y_ann-50 ones(nr_ann,1)*100 ones(nr_ann,1)*100];

% Format [frame_nr x y width height score]
dets = detections;

% Get thresholds
max_threshold = max(dets(:, 6));
min_threshold = min(dets(:, 6));

acc = [];

N = 200;
if(min_threshold > 0)
    steps =  (max_threshold+min_threshold)/N;
else
    steps =  (max_threshold-min_threshold)/N;
end

% For SPU, loop over each step
%steps = 1;

% Loop over scores
for thresh = min_threshold:steps:max_threshold

display(['Looping over threshold: ' num2str(thresh) ' of ' num2str(max_threshold) '.']);

threshold = thresh;

TP_total = 0;
FP_total = 0;
FN_total = 0;

% Remove detections with score lower than threshold
indices = dets(:, 6) >= threshold;

dets_for_thresh = dets(indices, :);
dets_for_thresh = dets_for_thresh(:, 2:5);

% Calculate the accuracy for this frame
if(isempty(ann))
    TP = 0;
    FN = 0;
    FP = size(dets_for_thresh, 1);
else
    if(isempty(dets))
        TP = 0;
        FP = 0;
        FN = size(ann, 1);
    else
        [TP, FP, FN] = calc_acc(ann, dets_for_thresh, overlap);
    end
end

acc = [acc; threshold TP FP FN];
end

TP
FP
FN

Precision = TP / (TP + FP)
Recall = TP / (TP + FN)

Overall_accuracy = (Precision + Recall) / 2


save(['accuracy_results/' model_name '.mat'], 'acc');





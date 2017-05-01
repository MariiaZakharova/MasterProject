function [TP, FP, FN] = calc_acc(ann_reformed, det_reformed, overlap)
% Calculate the accuracy for a specific frame

% Compare each detection with each annotation
nr_ann = size(ann_reformed, 1);
nr_det = size(det_reformed, 1);

TP = 0;
FP = 0;
FN = 0;

% Keep detection for FP
is_linked = zeros(nr_det, 1);

% Loop over detections
for i = 1:nr_det
    if(mod(i, 1000) == 0)
        display(['Processing detection ' num2str(i) ' of ' num2str(nr_det) '.'])
    end
    det = det_reformed(i, :);
    
    % Compare with all annotations
    for j = 1:size(ann_reformed, 1)
        ann = ann_reformed(j, :);
        
        % If this is the same detection, it is a TP, confirm detection is linked, break and eliminate
        % annotation
        if(same_detection(det, ann, overlap))
            TP = TP + 1;
            is_linked(i) = 1;
            ann_reformed(j, :) = [];
            break
        end     
    end
end

% All not linked detections are FP
FP = sum(is_linked == 0);

% All remaining annotations are FN
FN = size(ann_reformed, 1);

end


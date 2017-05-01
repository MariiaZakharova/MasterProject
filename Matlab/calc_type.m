function [TP, FP, FN, bb_tp, bb_fp, bb_fn] = calc_type(ann_reformed, det_reformed, overlap)
% Calculate the accuracy for a specific frame

% Compare each detection with each annotation
nr_ann = size(ann_reformed, 1);
nr_det = size(det_reformed, 1);

TP = 0;
FP = 0;
FN = 0;
bb_tp = [];
bb_fp = [];
bb_fn = [];

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
            bb_tp = [bb_tp; det];
            is_linked(i) = 1;
            ann_reformed(j, :) = [];
            break
        end     
    end
end

% All not linked detections are FP
FP = sum(is_linked == 0);
bb_fp = det_reformed(logical(~is_linked), :);

% All remaining annotations are FN
FN = size(ann_reformed, 1);
bb_fn = ann_reformed;

end


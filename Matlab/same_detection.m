function output = same_detection(det1, det2, overlap)

x11 = det1(1); y11 = det1(2);
x12 = x11 + det1(3) ; y12 = y11 + det1(4);

x21 = det2(1); y21 = det2(2);
x22 = x21 + det2(3) ; y22 = y21 + det2(4);

x_overlap = max(0,min(x12,x22)-max(x11,x21));
y_overlap = max(0,min(y12,y22)-max(y11,y21));

surfdet1 = det1(3)*det1(4);
surfdet2 = det2(3)*det2(4);
surfoverlap = x_overlap*y_overlap;

if(surfoverlap > overlap*surfdet1 && surfoverlap > overlap*surfdet2)
    output = 1;
else
    output = 0;
end

end


function ap = calc_ap(new_R_raw, new_P_raw)

% Calculate the AP
R = new_R_raw;
P = new_P_raw;

ap = sum(P(2:end).*abs(diff(R)));

end


%Load accuracy results
load('accuracy_results/coconut_model1.mat');

P = acc(:, 2)./(acc(:, 2) + acc(:, 3));
R = acc(:, 2)./(acc(:, 2) + acc(:, 4));

ap_vector = [];

figure(2),clf;
plot(R, P, 'color', 'r', 'linewidth', 2);
grid on;
axis([0 1.01 0 1.01]);
ap = calc_ap(R(1:end-1),P(1:end-1))
ap_vector = [ap_vector ap];

hold on;
lg_text = {['Coconut Model 1, AP = ' num2str(ap_vector(1)*100, 4) '%']};
legend(lg_text, 'location', 'sw');




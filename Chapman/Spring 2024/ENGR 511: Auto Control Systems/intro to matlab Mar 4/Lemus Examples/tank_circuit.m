%variable setup
R=1; L=1; C=1;
G = tf([1/(R*C) 0], [1 1/(R*C) 1/(L*C)]);

bode(G), grid

R1 = 5; G1 = tf([1/(R1*C) 0], [1 1/(R1*C) 1/(L*C)]);
R2 = 20; G2 = tf([1/(R2*C) 0], [1 1/(R2*C) 1/(L*C)]);

bode(G, 'b',G1, 'r', G2, 'g'), grid
legend('R=1','R=5','R=20')
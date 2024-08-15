% rlcdemo

s=tf('s')

K = 10

sysT = (K*(s+1))/(s^3+(5*s^2)+((K-6)*s)+K);
step(sysT)
pzplot(sysT)
denT = [1 5 K-6 K]
roots(denT)
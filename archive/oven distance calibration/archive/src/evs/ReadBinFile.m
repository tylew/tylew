%mex -g ReadBinFile.cpp

NrOfFrames = 1;
NrOfShots = 164000;
RxRowMax = 86;
RxColMax = 166
NrOfShots = 16000;

filename = '..\test\lutTest.bin';
% call cpp function 
[data,errorCode] = ReadBinFile(filename,1,NrOfShots);
data1Frames = reshape(data(1,:,:),NrOfShots,8);
data2d = zeros(86,166);
for i = 1:NrOfShots
    RxColAct = data1Frames(i,5)+1;
    RxRowAct = data1Frames(i,6)+1;
    data2d(RxColAct,RxRowAct) = data1Frames(i,1);
end
save('data1Frames.mat', 'data1Frames');
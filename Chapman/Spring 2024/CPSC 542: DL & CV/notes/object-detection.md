
Goal of OD is to define bounding boxes around identified locations within an image.

bx, by, bw, bh, C


## R-CNN
Graph based segmentation for region proposals
Bounding box regression: non-linear LS
Classification: SVMs (binary linear SVM per class)

## Fast R-CNN
Combine BB regression + classification, optimize over the two simultaneously


## Faster R-CNN
Region proposal networkx

How is object detection done and what sort of optimizations can be done?
import numpy


def calculate(data, baseline, baselag, cusumFlag, cusumK, minSigma, thresh):
    """
    function to implement ears algorithm

    data: list of numbers of on which algorithm is applied
    baseline: 7 days for each algorithm
    baselag: 0 for C1 and 2 for both C2 and C3
    cusumFlag: 0 for both C1 and C2 and 1 for C3
    cusumK: 1 for all C1, C2 and C3
    minSigma: 0.1 for all C1, C2 and C3
    thres: 2 for all C1, C2 and C3

    Returns two sets of list:
    earStat: returns same number of data as original list with ears value
    curr: returns list whih consists of same values as earStat but removing
        the unwanted inital 7 days value for C1 and 9 days value for C2 and C3
    """
    earstat = [0] * len(data)
    cusum0 = 0
    cusum1 = 0
    ndxBase = 0
    estMean = 0
    estSigma = 0
    currSum = 0
    curr = []
    for i in range(baseline + baselag, len(data)):
        ndxBase = i - (baseline + baselag)
        new_list = []
        for j in range(baseline):
            new_list.append(data[ndxBase])
            ndxBase = ndxBase + 1
        estMean = numpy.mean(new_list)
        list_std = numpy.std(new_list)
        estSigma = max(minSigma, list_std)
        try:
            currSum = max(0, data[i] - estMean - cusumK * estSigma) / estSigma
        except:
            currSum = 0
        curr.append(currSum)
        earstat[i] = currSum + cusumFlag * (cusum0 + cusum1)
        cusum0 = cusum1
        if currSum >= thresh:
            cusum1 = 0
        else:
            cusum1 = currSum
    return earstat, curr


def calculateC1(data):
    return calculate(data, 7, 0, 0, 1, .1, 2)


def calculateC2(data):
    return calculate(data, 7, 2, 0, 1, .1, 2)


def calculateC3(data):
    return calculate(data, 7, 2, 1, 1, .1, 2)

inp = [6, 142, 124, 145, 9, 6, 184, 130, 140, 136, 136, 20, 3, 169, 170, 134, 106,
                         181, 22, 1, 7, 233, 196, 153, 155, 19, 2, 277, 198, 192, 191, 218, 25, 4,
                         281, 161, 199, 182, 197, 19, 15, 272, 235, 227, 169, 153, 34, 7, 8, 299,
                         210, 135, 135, 18, 12, 163, 120, 85, 91, 87, 17, 3, 167, 130, 86, 87, 88,
                         11, 5, 128, 103, 86, 10154, 79, 13, 4, 113, 92, 82, 85, 59, 16, 9, 101, 100,
                         76, 68, 83, 7, 5, 110, 98, 60, 37, 91, 6, 1, 53, 87, 115, 93, 83, 8, 4, 126,
                         96, 84, 73, 67, 6, 3, 143, 88, 90, 92, 109, 8, 2, 150, 130, 91, 93, 101, 3,
                         0, 157, 119, 106, 104, 84, 6, 1, 140, 100, 90, 51, 92, 9, 2, 111, 103, 95,
                         89, 46, 16, 3, 1, 78, 77, 78, 59, 4, 2, 69, 70, 61, 53, 47, 5, 0, 68, 75,
                         55, 49, 42, 2, 1, 45, 44, 38, 32, 39, 6, 0, 62, 53, 39, 42, 39, 3, 2, 45,
                         44, 30, 1, 1, 6, 2, 32, 33, 13, 16, 34, 6, 0, 39, 30, 26, 21, 21, 4, 1, 29,
                         34, 20, 25, 21, 3, 3, 44, 1];
print len(calculateC2(inp)[0]), len(inp)
print calculateC2(inp)[0]
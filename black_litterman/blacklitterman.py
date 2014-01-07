def calc_mean(data):
    return sum(data)/len(data)

def stddev(data):
    mean = calc_mean(data)
    summation = 0
    for x in data:
        summation += (x - mean) ** 2
    return math.sqrt(summation/len(data))

def correl_matrix(assets):
    corr_matrix = np.zeroes(len(assets), len(assets))
    for i in range(len(assets)):
        for j in range(len(assets)):
            corr_matrix[i][j] = numpy.correlate(assets[i], assets[j])
            corr_matrix[j][i] = numpy.correlate(assets[i], assets[j])

    return corr_matrix 

def stddev_matrix(assets):
    #assumes len(assets) = num of assets
    #len(assets[0]) = length of time series
    dev_matrx = np.zeros(len(assets), len(assets))
    for x in range(len(assets)):
        dev_matrix[x][x] = stddev(assets[x] * 16) #annualized, 256 days in a year

    return dev_matrix



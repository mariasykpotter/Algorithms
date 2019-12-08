def knapsackHelper(items, w, itemIndex, itemIndexCapacityValueMatrix):
    if w == 0 or itemIndex == len(items):
        return [0, 0]
    itemValue = items[itemIndex][0]
    itemWeight = items[itemIndex][1]
    if itemWeight > w:
        return makeRecursiveCallIfNeeded(items, w, itemIndex + 1, itemIndexCapacityValueMatrix)
    maxValueItemsUsedPair = makeRecursiveCallIfNeeded(items, w - itemWeight, itemIndex + 1,
                                                      itemIndexCapacityValueMatrix)
    maxValueWithItemUsed = [itemValue + maxValueItemsUsedPair[0], maxValueItemsUsedPair[1] * 10 + itemIndex]
    maxValueWithoutItemUsed = makeRecursiveCallIfNeeded(items, w, itemIndex + 1, itemIndexCapacityValueMatrix)
    tmpMax = max(maxValueWithItemUsed[0], maxValueWithoutItemUsed[0])
    if (tmpMax == maxValueWithItemUsed[0] and tmpMax != maxValueWithoutItemUsed[0]):
        itemIndexCapacityValueMatrix[itemIndex][w] = maxValueWithItemUsed
    else:
        itemIndexCapacityValueMatrix[itemIndex][w] = maxValueWithoutItemUsed
    return itemIndexCapacityValueMatrix[itemIndex][w]


def makeRecursiveCallIfNeeded(items, w, itemIndex, itemIndexCapacityValueMatrix):
    if itemIndexCapacityValueMatrix[itemIndex][w] == 0:
        itemIndexCapacityValueMatrix[itemIndex][w] = knapsackHelper(items, w, itemIndex, itemIndexCapacityValueMatrix)
    return itemIndexCapacityValueMatrix[itemIndex][w]


def knapsack(items, maxWeight):
    if len(items) < 500:
        items = [x for x in items if x[1] <= maxWeight]
        itemIndexCapacityValueMatrix = [[0 for x in range(maxWeight + 1)] for y in range(len(items) + 1)]
        maxValueItemsUsedPair = knapsackHelper(items, maxWeight, 0, itemIndexCapacityValueMatrix)
        itemsUsed = maxValueItemsUsedPair[1]
        asList = [int(x) for x in str(itemsUsed)]
        return maxValueItemsUsedPair[0], asList
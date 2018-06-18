import numpy as np

axes = [np.array([0,1])]
axes.append(np.array([1,0]))
axes.append(np.array([1,1]))
axes.append(np.array([1,-1]))
axes[2]= axes[2]/np.linalg.norm(axes[2])
axes[3]= axes[3]/np.linalg.norm(axes[3])

def projectOntoAxis(vertices, axis):
    """ Projects the shape defined by the vertices into the given axis """
    min= np.dot(axis,vertices[0])
    max= min
    for i in range(len(vertices)):
        proj = np.dot(axis, vertices[i])
        min =proj if proj < min else min
        max = proj if proj> max else max
    return min,max

def sat(vertices0, vertices1):
    """ Returns true if the rectangles overlap using Separating Axes Theorem """
    for axis in axes:
        min1, max1 = projectOntoAxis(vertices0, axis)
        min2,max2 = projectOntoAxis(vertices1, axis)
        if not (min1 <= min2 < max1) and not (min2 <= min1 < max2):
            return False
    return True

def test():
    vertices0 = [np.array([2,2]), np.array([2,0]), np.array([4,0]), np.array([4,4])]
    vertices1 = [np.array([3,3]), np.array([3,0]), np.array([0,0]), np.array([0,3])]

    print(sat(vertices0, vertices1))

    vertices1 = [np.array([1,1]), np.array([1,0]), np.array([0,0]), np.array([0,1])]

    print(sat(vertices0, vertices1))


if __name__ == '__main__':
    test()
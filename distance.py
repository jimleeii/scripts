import arcpy

xs = [-114.598413495,-114.587314575,-114.586034308,-114.582077209,-114.580337087,-114.580306684,-114.576597046,-114.57575007]
ys = [52.966152304,52.9664493280001,52.9674172150001,52.9674234240001,52.9674089310001,52.966810599,52.9662992240001,52.966134777]
ms = [1211.4261,1957.2668,2065.08040000001,2330.90029999999,2447.79760000001,2488.0426,2739.59540000001,2797.55379999999]

total_distance = 0
index = 0
for i in range(1, len(xs)):
    # Create the first point
    point1 = arcpy.Point(xs[index], ys[index])

    # Create the second point
    point2 = arcpy.Point(xs[i], ys[i])

    # Create a spatial reference object (if needed)
    spatial_reference = arcpy.SpatialReference(4326)  # Update with the appropriate spatial reference

    # Create the first point geometry
    point1_geometry = arcpy.PointGeometry(point1, spatial_reference)

    # Create the second point geometry
    point2_geometry = arcpy.PointGeometry(point2, spatial_reference)

    # Calculate the distance between the points
    distance = point1_geometry.angleAndDistanceTo(point2_geometry, 'GEODESIC')

    m_distance = ms[i] - ms[index]

    total_distance = total_distance + distance[1]

    # Print the results
    print("Angle between the {} and {} points: {:.2f} degrees".format(index, i, distance[0]))
    print("Distance between the {} and {} points: {:.9f} meters".format(index, i, distance[1]))
    print("M distance between the {} and {} points: {:.9f} meters".format(index, i, m_distance))
    print("Ratio between the {} and {} points: {:.9f} meters".format(index, i, m_distance / distance[1]))

    index = index + 1

print((ms[7] - ms[0]) / total_distance, total_distance)
exit(0)

# import math

# Calculate the difference in x and y coordinates
dx = point2.X - point1.X
dy = point2.Y - point1.Y

# Calculate the distance between the points
distance_math = math.sqrt(dx**2 + dy**2)

# Calculate the angle between the points in radians
angle_rad = math.atan2(dy, dx)

# Convert the angle to degrees
angle_deg = math.degrees(angle_rad)

# Print the results
print("Distance between the points: {:.2f} units".format(distance_math))
print("Angle between the points: {:.2f} degrees".format(angle_deg))
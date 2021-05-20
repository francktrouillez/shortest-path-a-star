from InstancesGenerator import InstancesGenerator


if __name__ == "__main__":
    instanceGenerator = InstancesGenerator(numberOfNodes = 100, minX = 0, minY = 0, maxX = 200, maxY = 200, probabilityOfStrangeMove = 0.01, minConnexions = 1, maxConnexions = 5, minRadius = 10, maxRadius = 40)
    instanceGenerator.generate("testInstance.txt")

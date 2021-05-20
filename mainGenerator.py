from InstancesGenerator import InstancesGenerator


if __name__ == "__main__":
    instanceGenerator = InstancesGenerator(numberOfNodes = 2000, minX = 0, minY = 0, maxX = 300, maxY = 300, probabilityOfStrangeMove = 0.00, minConnexions = 1, maxConnexions = 10, minRadius = 5, maxRadius = 10)
    instanceGenerator.generate("testInstance.txt")

import platform, sys

distr = platform.linux_distribution()
print distr[1].split('.')[0]

sys.exit(0)


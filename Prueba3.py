# Importing necessary libraries
import pandas as pd

# Load the dataset
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")

# TASK 1: Calculate the number of launches on each site
launch_site_counts = df['LaunchSite'].value_counts()
print("Number of launches on each site:")
print(launch_site_counts)
print()

# TASK 2: Calculate the number and occurrence of each orbit
orbit_counts = df['Orbit'].value_counts()
print("Number and occurrence of each orbit:")
print(orbit_counts)
print()

# TASK 3: Calculate the number and occurrence of mission outcome per orbit type
landing_outcomes = df['Outcome'].value_counts()
print("Number and occurrence of mission outcomes:")
print(landing_outcomes)
print()

# Create a set of bad outcomes where the second stage did not land successfully
bad_outcomes = set(landing_outcomes.keys()[[1, 3, 5, 6, 7]])

# TASK 4: Create a landing outcome label from Outcome column
landing_class = []

for outcome in df['Outcome']:
    if outcome in bad_outcomes:
        landing_class.append(0)
    else:
        landing_class.append(1)

# Add the landing class as a new column in the DataFrame
df['Class'] = landing_class

# Calculate the success rate of launch
success_rate = df["Class"].mean()
print("Success rate of launch:", success_rate)
print()

# Export the data to a CSV file
df.to_csv("dataset_part_2.csv", index=False)

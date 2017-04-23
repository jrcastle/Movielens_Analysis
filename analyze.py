import math
import scipy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab

# Pandas dataframes for the three .dat files

print "Loading movies.dat ..."
dfMovies = pd.read_table("movies.dat", 
                   sep='::', 
                   engine="python", 
                   header=None
                   )
dfMovies.columns = ['MovieID', 'Title', 'Genres']

print "Loading ratings.dat ..."
dfRatings = pd.read_table("ratings.dat",
                          sep='::',
                          engine="python",
                          header=None
                          )
dfRatings.columns = ['UserID', 'MovieID', 'Rating', 'Timestamp']

print "Loading users.dat ..."
dfUsers = pd.read_table("users.dat",
                        sep='::',
                        engine="python",
                        header=None
                        )
dfUsers.columns = ['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code']

# Merge dataframes
dfMerged = pd.merge(dfRatings, dfUsers, how = 'outer')
dfFinal  = pd.merge(dfMerged, dfMovies, how = 'outer')
del dfMerged

# Dictionary that maps occupation code to occupation
occupations = {}
occupations[0]  = "Other"
occupations[1]  = "Academic/educator"
occupations[2]  = "Artist"
occupations[3]  = "Clerical/admin"
occupations[4]  = "College/grad student"
occupations[5]  = "Customer service"
occupations[6]  = "Doctor/health care"
occupations[7]  = "Executive/managerial"
occupations[8]  = "Farmer"
occupations[9]  = "Homemaker"
occupations[10] = "K-12 student"
occupations[11] = "Lawyer"
occupations[12] = "Programmer"
occupations[13] = "Retired"
occupations[14] = "Sales/marketing"
occupations[15] = "Scientist"
occupations[16] = "Self-employed"
occupations[17] = "Technician/engineer"
occupations[18] = "Tradesman/craftsman"
occupations[19] = "Unemployed"
occupations[20] = "Writer"

# Dictionary that maps age code to age group
ageGroup = {}
ageGroup[1]  = "Under 18"
ageGroup[18] = "18-24"
ageGroup[25] = "25-34"
ageGroup[35] = "35-44"
ageGroup[45] = "45-49"
ageGroup[50] = "50-55"
ageGroup[56] = "56+"

# Explore the distribution of occupations who responded #########################################
occupation_list = dfUsers["Occupation"].tolist()
bin_boundaries = [i+0.5 for i in range(-1,21)]

fig = plt.hist(occupation_list, bins=bin_boundaries) 
ax = plt.subplot(111)

# x axis
ax.set_xlabel("Occupation")
ax.set_xlim(-1,21)
x =  [i for i in range(0,21)]
xl = [occupations[i] for i in range(0,21)]
plt.xticks(x, xl, rotation='vertical')
plt.tick_params(axis='x', which='major', labelsize=9)
plt.gcf().subplots_adjust(bottom=0.35)

# y axis
ax.set_ylabel("Count")

# save plot
plt.savefig('plots/OccupationDist.pdf')
plt.close()
# Explore the distribution of ratings for different occupations #################################
bin_boundaries = [i+0.5 for i in range(-1,6)]
for occ in occupations:
    occupation_ratings = dfFinal.loc[dfFinal["Occupation"] == occ, "Rating"].tolist()
    fig = plt.hist(occupation_ratings, bins=bin_boundaries), 
    ax = plt.subplot(111)

    # x axis
    ax.set_xlabel("Rating")
    ax.set_xlim(0,6)
    # y axis
    ax.set_ylabel("Count")
    # title
    name = occupations[occ] + " Distribution of Ratings"
    plt.title(name)
    # save plot
    name = 'plots/%sRatings.pdf' % (occupations[occ].replace("/", "_"))
    name = name.replace(" ", "")
    print name + " created!"
    plt.savefig(name)
    plt.close()
#ENDFOR


#bin_boundaries = [i+0.5 for i in range(-1,6)]
#for occ in occupations:
#
#    if occ not in occupation_ratings:
#        continue
#    #ENDIF
#    fig, ax = plt.subplots()
#    plt.hist(occupation_ratings[occ], bins=bin_boundaries)
#
#    # x axis
#    ax.set_xlabel("Rating")
#    ax.set_xlim(0,6)
#    # y axis
#    ax.set_ylabel("Count")
#    # title
#    name = occupations[occ] + " Distribution of Ratings"
#    plt.title(name)
#    # save plot
#    name = 'plots/%sRatings.pdf' % (occupations[occ].replace("/", "_"))
#    name = name.replace(" ", "")
#    print name + " created!"
#    plt.savefig(name)
##ENDFOR

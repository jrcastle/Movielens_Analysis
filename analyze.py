import math
import os
import scipy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab

# Flags on what to analyze
block0 = 1  # Explore the distribution of occupations who responded
block1 = 1  # Explore the distribution of ratings for different occupations
block2 = 1  # Explore the average rating for a genre for all occupations

# Clean the plots directory
#print "Cleaning the plots directory..."
#command = "rm plots/*.pdf"
#os.system(command)

# Pandas dataframes for the three .dat files
if not os.path.isfile( "MergedDataset.csv" ):
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
    print "Merging dataframes ..."
    dfMerged = pd.merge(dfRatings, dfUsers, how = 'outer')
    dfFinal  = pd.merge(dfMerged, dfMovies, how = 'outer')
    del dfMerged

    dfFinal.to_csv("MergedDataset.csv")
else:
    print "Loading MergedDataset.csv ..."
    dfFinal = pd.read_csv("MergedDataset.csv",
                          engine="python"
                          )

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

# List containing all possible genres in the dataset
genres = [
    "Action",
    "Adventure",
    "Animation",
    "Children\'s",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Fantasy",
    "Film-Noir",
    "Horror",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
    "War",
    "Western"]

# Explore the distribution of occupations who responded #########################################
if block0:
    dfUsers = pd.read_table("users.dat",
                            sep='::',
                            engine="python",
                            header=None
                            )
    dfUsers.columns = ['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code']

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

    del dfUsers
#ENDIF

# Explore the distribution of ratings for different occupations #################################
if block1:
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
        name = 'plots/OccupationDistnOfRatings/%sRatings.pdf' % (occupations[occ].replace("/", "_"))
        name = name.replace(" ", "")
        print name + " created!"
        plt.savefig(name)
        plt.close()
    #ENDFOR
#ENDIF

# Explore the average rating for a genre for all occupations/ages #################################
if block2:
    for gen in genres:

        # Occupation
        x =  [i for i in range(0,len(occupations))]
        xl = [occupations[i] for i in range(0,len(occupations))]
        y  = []
        ye = []
        for occ in occupations:
            occupation_ratings = dfFinal.loc[ (dfFinal["Occupation"] == occ) & (dfFinal["Genres"].str.contains(gen)), "Rating"].tolist()
            occupation_ratings = np.array(occupation_ratings)
            ave_rating = np.average( occupation_ratings )
            std_rating = np.std( occupation_ratings )
            y.append(ave_rating)
            ye.append(std_rating)
            #print "Average Rating = " + str(ave_rating)
        #ENDFOR

        fig = plt.bar(x, y, 1, yerr = ye),
        ax = plt.subplot(111)

        # x axis
        ax.set_xlabel("Occupation")
        ax.set_xlim(-1,len(occupations))
        plt.xticks(x, xl, rotation='vertical')
        plt.tick_params(axis='x', which='major', labelsize=9)
        plt.gcf().subplots_adjust(bottom=0.35)

        # y axis
        ax.set_ylabel("Average Rating")
        ax.set_ylim(0,5)

        # title
        name = gen + " Genre: Average Rating Per Occupation"
        plt.title(name)

        # save plot
        name = 'plots/GenreAveRatingVSOccupation/Genre%s_AveRating_VS_occupation.pdf' % gen.replace("\\'", "")
        name = name.replace(" ", "")
        print name + " created!"
        plt.savefig(name)
        plt.close()

        # Age group
        x =  [i for i in range(0,len(ageGroup))]
        xl = [ageGroup[i] for i in sorted(ageGroup.keys())]
        y  = []
        ye = []
        for age in ageGroup:
            age_ratings = dfFinal.loc[ (dfFinal["Age"] == age) & (dfFinal["Genres"].str.contains(gen)), "Rating"].tolist()
            age_ratings = np.array( age_ratings )
            ave_rating = np.average( age_ratings )
            std_rating = np.std( age_ratings )
            y.append(ave_rating)
            ye.append(std_rating)
        #ENDFOR

        fig = plt.bar(x, y, 1, yerr = ye),
        ax = plt.subplot(111)

        # x axis
        ax.set_xlabel("Age Group")
        ax.set_xlim(-1,len(ageGroup))
        plt.xticks(x, xl)#, rotation='vertical')
        plt.tick_params(axis='x', which='major', labelsize=9)
        plt.gcf().subplots_adjust(bottom=0.15)

        # y axis
        ax.set_ylabel("Average Rating")
        ax.set_ylim(0,5)

        # title
        name = gen + " Genre: Average Rating Per Age Group"
        plt.title(name)

        # save plot
        name = 'plots/GenreAveRatingVSAge/Genre%s_AveRating_VS_Age.pdf' % gen.replace("\\'", "")
        name = name.replace(" ", "")
        print name + " created!"
        plt.savefig(name)
        plt.close()

    #ENDFOR
#ENDIF

#################################  TODO #################################
# Remove the apostrophy in Children's when saved to pdf
# Try to speed up the average rating calculations.  Maybe try making a smaller dataframe and then slicing that? 
#
# Explore average rating for a genre for each gender
#   * two color plot Ave rating VS genre where each color is a gender


# Implementation URL
# https://blog.opavote.com/2016/11/plain-english-explanation-of-scottish.html

# View Video Explanation
# https://www.fairvote.org/rcv#how_rcv_works (bottom video on "multi-winner")

# Building the CSV File:
# Candidate Names Should Be Assigned Randomly from Left to Right
# Left-Most of Multiple-Tied Candidated will be Elected/Eliminated
#    in the event of a round #1 tie

# Coded in Python 3.4.3 on Windows 10 PC

import csv
import math
import sys
import pdb

# File to pull from
inputFile = "rc_votes.csv"

# Read in Candidate List and Raw Ballots from CSV File
def getCandidates():

    fileData = csv.reader(open(inputFile,'rt'))

    # Load candidates in dictionary for tracking.
    candidates = []
    [candidates.append({'name': name, 'prevTally': 0, 'tally': 0, 'status': ''}) for name in next(fileData)]

    # Read ballots in to 2d list of integers
    ballots = []
    [ballots.append(list(map(str.strip, row))) for row in fileData]
    ballots = [[int(y) for y in x] for x in ballots]

    return [candidates, ballots]


# Round
# Surplus votes are distributed
# If candidate reaches:
#   It is top vote getter
#   Candidate ahead in previous round if dead tie
#   Candidate left to right if tie in first round
#   Surplus votes are calculated
# If no candidate reaches, bottom is eliminated
#   Winner is determined based on redistribution.
#   Surplus votes are calculated 

def processVotingData(candidates, ballots, electionThreshold):

    # Loop through the rounds
    voteRound = 1
    amountToDistribute = 0
    while voteRound < len(candidates):

        # Distribute surplus votes or tally first round.
        if voteRound > 1:
            # Note the previous tally
            for candidate in candidates:
                candidate['prevTally'] = candidate['tally']
            # Distribute extra votes
            for ballot in ballots:
                if ballot.index(voteRound-1) == i and candidates[ballot.index(voteRound)]['status'] == "":
                    candidates[ballot.index(voteRound)]['tally'] += amountToDistribute
        else:
            # Loop through the ballots and tally up the votes.
            for ballot in ballots:
                candidates[ballot.index(voteRound)]['tally'] += 1


        # Determine if there is a winner.
        tallies = [candidate['tally'] for candidate in candidates]
        maxVotes = [i for i, x in enumerate(tallies) if x == max(tallies)]

        if candidate[maxVotes[0]]['tally'] > electionThreshold:
            # There is a winner

        else:
            # There isn't a winner
            # Determine lowest tally.
            tallies = [abs(candidate['tally']) for candidate in candidates]
            minVotes = [i for i, x in enumerate(tallies) if x == min(tallies)]

            # Remove the candidates and note the amount to distribute.
            candidates[minVotes[-1]]['status'] = 'Removed in round ' + str(voteRound)
            amountToDistribute = candidates[minVotes[-1]]['tally']
            candidates[minVotes[-1]]['tally'] = -999
        

        # Loop through and note any winners.
        winner = False
        for i in range(len(candidates)):
            if candidates[i]['status'] == "" and candidates[i]['tally'] >= electionThreshold:
                
                winner = True

                # Note the votes to distribute and reduce candidate tally by that amount.
                totalVotesToDistribute = candidates[i]['tally'] - electionThreshold
                amountToDistribute = totalVotesToDistribute / candidates[i]['tally']
                candidates[i]['tally'] = -999

                # Lock the candidate record so that it is ignored in the future.
                candidates[i]['status'] = 'Winner Round ' + str(voteRound) + ', #' + str(winnerNumber)
                winnerNumber += 1

                


        print('----------------')
        print("Round: " + str(voteRound))
        print(candidates)
        print('----------------')

        voteRound += 1
            
    return candidates

def main():
    
    # Get the data
    seat_count = int(input("Number of seats:"))
    print('===============================================================================================================================')
    [candidates, ballots] = getCandidates()
    ballot_count = len(ballots)
    electionThreshold = math.floor((ballot_count / (seat_count + 1)) + 1) # DO NOT CHANGE
    
    # Determine winners
    candidates = processVotingData(candidates,ballots,electionThreshold)

    print("Candidates found:  " + str(len(candidates)))
    print("Ballots:",ballot_count)
    print("Threshold:",electionThreshold)
    print("Results:")
    for candidate in candidates:
        print(candidate['name'] + ' ' + candidate['status'])
        
    return 0


if __name__ == '__main__':
    sys.exit(main())
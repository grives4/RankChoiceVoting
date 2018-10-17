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
import pprint

# File to pull from
inputFile = "rc_votes.csv"

# Read in Candidate List and Raw Ballots from CSV File
def getVotes(seat_count):

    fileData = csv.reader(open(inputFile,'rt'))

    # Load candidates in dictionary for tracking.
    candidates = {}
    names = []
    for name in next(fileData):
        candidates[name] = {'prevTally': 0, 'tally': 0, 'status': ''}
        names.append(name)

    # Read ballots in to 2d list of integers
    ballots = []
    [ballots.append(list(map(str.strip, row))) for row in fileData]
    ballots = [[int(y) for y in x] for x in ballots]

    # Do a quick check of the ballots
    validateBallots(seat_count, ballots)
    
    # Add names and sort names by vote per ballot
    votes = []
    for ballot in ballots:
        vote = [''] * seat_count
        for i in range(len(ballot)):
            if ballot[i] != 0:
                vote[ballot[i]-1] = names[i]

        votes.append(vote)
    pprint.pprint(votes)
    return [candidates, votes]

def convertToVoteStack(candidates, ballots):
    voteStack = []


def validateBallots(seat_count, ballots):
    
    # Validate the data
    ballotRow = 1
    validBallotCounts = [1,3,6,10,15,21]
    for ballot in ballots:
        if not sum(ballot) in validBallotCounts[:seat_count]:
            print("Warning!  Make sure ballot on row " + str(ballotRow) + " is correct.")
            input()
        ballotRow += 1
       
    return 

# Round
# If candidate reaches:
#   It is top vote getter
#   Candidate ahead in previous round if dead tie
#   Candidate left to right if tie in first round
#   Surplus votes are calculated
#   Surplus votes are distributed
# If no candidate reaches, bottom is eliminated
#   Winner is determined based on redistribution.
#   Surplus votes are calculated 
#   Surplus votes are distributed

def processVotingData(candidates, votes, electionThreshold, seat_count):

    # Loop through the rounds
    roundOne = True
    amountToDistribute = 0
    winnerNumber = 1
    lastWinner = 0
    while winnerNumber < seat_count:

        # Tally first round.
        if roundOne:
            for vote in votes:
                candidates[vote[i]]['tally'] = 1
            roundOne = False

        # Determine if there is a winner.
        tallies = [candidate['tally'] for candidate in candidates]
        maxVotes = [i for i, x in enumerate(tallies) if x == max(tallies)]

        if candidates[maxVotes[0]]['tally'] > electionThreshold:
            # There is a winner
            # Note the votes to distribute and reduce candidate tally by that amount.
            totalVotesToDistribute = candidates[maxVotes[0]]['tally'] - electionThreshold
            amountToDistribute = totalVotesToDistribute / candidates[maxVotes[0]]['tally']
            candidates[maxVotes[0]]['tally'] = -999

            # Lock the candidate record so that it is ignored in the future.
            candidates[maxVotes[0]]['status'] = 'Winner Round ' + str(voteRound) + ', #' + str(winnerNumber)
            lastWinner = maxVotes[0]
            winnerNumber += 1


            # Note the previous tally
            for candidate in candidates:
                candidate['prevTally'] = candidate['tally']
            # Distribute extra votes
            for ballot in ballots:
                if ballot.index(voteRound-1) == lastWinner and candidates[ballot.index(voteRound)]['status'] == "":
                    candidates[ballot.index(voteRound)]['tally'] += amountToDistribute
            



        else:
            # There isn't a winner
            # Determine lowest tally.
            tallies = [abs(candidate['tally']) for candidate in candidates]
            minVotes = [i for i, x in enumerate(tallies) if x == min(tallies)]

            # Remove the candidates and note the amount to distribute.
            candidates[minVotes[-1]]['status'] = 'Removed in round ' + str(voteRound)
            amountToDistribute = candidates[minVotes[-1]]['tally']
            candidates[minVotes[-1]]['tally'] = -999

            
        
        print('----------------')
        print("Round: " + str(voteRound))
        pprint.pprint(candidates)
        #for candidate in candidates:
        #    print(candidate['name'] + ' ' + candidate['status'])
        print('----------------')

        voteRound += 1
            
    return candidates

def main():
    
    # Get the data
    seat_count = int(input("Number of seats:"))
    print('===============================================================================================================================')
    [candidates, votes] = getVotes(seat_count)
    
    ballot_count = len(votes)
    electionThreshold = math.floor((ballot_count / (seat_count + 1)) + 1) # DO NOT CHANGE
    
    # Determine winners
    candidates = processVotingData(candidates,votes,electionThreshold, seat_count)

    print("Candidates found:  " + str(len(candidates)))
    print("Ballots:",ballot_count)
    print("Threshold:",electionThreshold)
    print("Results:")
    for candidate in candidates:
        print(candidate['name'] + ' ' + candidate['status'])

    return 0


if __name__ == '__main__':
    sys.exit(main())
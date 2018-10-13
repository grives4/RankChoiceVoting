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
    [candidates.append({'name': name, 'tally': 0, 'status': ''}) for name in next(fileData)]
    
    # Read ballots in to 2d list of integers
    ballots = []
    [ballots.append(list(map(str.strip, row))) for row in fileData]
    ballots = [[int(y) for y in x] for x in ballots]

    return [candidates, ballots]


def processVotingData(candidates, ballots, electionThreshold):
    
    winnerNumber = 1
    
    # Loop through the rounds
    voteRound = 1
    while voteRound < len(candidates):
        print("Round: " + str(voteRound))
        # Loop through the ballots and tally up the votes.
        for ballot in ballots:
            if candidates[ballot.index(voteRound)]['status'] == "":
                candidates[ballot.index(voteRound)]['tally'] += 1

        # Loop through and note any winners.
        nextRound = False
        while nextRound == False:
            winner = False
            for i in range(len(candidates)):
                if candidates[i]['status'] == "" and candidates[i]['tally'] >= electionThreshold:
                    
                    winner = True

                    # Note the votes to distribute and reduce candidate tally by that amount.
                    totalVotesToDistribute = candidates[i]['tally'] - electionThreshold
                    amountToDistribute = totalVotesToDistribute / candidates[i]['tally']
                    candidates[i]['tally'] = 999

                    # Lock the candidate record so that it is ignored in the future.
                    candidates[i]['status'] = 'Winner Round ' + str(voteRound) + ', #' + str(winnerNumber)
                    winnerNumber += 1

                    # Distribute the extra votes.
                    for ballot in ballots:
                        if ballot.index(voteRound) == i:
                            if candidates[ballot.index(voteRound+1)]['status'] == "":
                                candidates[ballot.index(voteRound+1)]['tally'] += amountToDistribute

                    print('----------------')
                    print(candidates)
                    print('----------------')

            if winner == False:
                # Determine lowest tally.
                minVotes = min([candidate['tally'] for candidate in candidates])

                # Determine who is last starting in reverse order of candidates.
                # Remove them and redistribute their votes.
                for i in reversed(range(len(candidates))):
                    if candidates[i]['tally'] == minVotes and candidates[i]['status'] == "":
                        candidates[i]['status'] = 'Removed in round ' + str(voteRound)
                        amountToDistribute = candidates[i]['tally']
                        candidates[i]['tally'] = 999

                        # Distribute the extra votes.
                        for ballot in ballots:
                            if candidates[ballot.index(voteRound)]['status'] == "":
                                candidates[ballot.index(voteRound)]['tally'] += amountToDistribute

                        break
                voteRound += 1
                nextRound = True
            else:
                nextRound = False

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
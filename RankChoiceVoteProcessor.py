# Implementation URL
# https://blog.opavote.com/2016/11/plain-english-explanation-of-scottish.html
# http://www.explore-2017.preflib.org/wp-content/uploads/2017/04/paper_16.pdf

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
inputFile = "rc_votes_1.csv"

# Read in Candidate List and Raw Ballots from CSV File
def getVotes(seat_count):

    fileData = csv.reader(open(inputFile,'rt'))

    # Load candidates in list for tracking.
    candidates = [{'name': name, 'prevTally': 0, 'tally': 0, 'status': ''} for name in next(fileData)]
    
    # Read ballots in to 2d list of integers
    ballots = [list(map(str.strip, row)) for row in fileData]
    ballots = [[int(y) for y in x] for x in ballots]

    # If weights were included, remove them.
    if candidates[0]['name'].lower() == 'weight':
        candidates.pop(0)
        for ballot in ballots:
            ballot.pop(0)

    # Do a quick check of the ballots
    validateBallots(seat_count, ballots)
    
    # Add names and sort names by vote per ballot
    # First column is the weight of the ballot
    votes = []
    weights = [1] * len(ballots)
    for ballot in ballots:
        vote = [''] * (seat_count + 1)
        vote[0] = '1.00000'
        for i in range(len(ballot)):
            if ballot[i] != 0:
                vote[ballot[i]] = candidates[i]['name']

        votes.append(vote)
    
    pprint.pprint(votes)
    
    return [candidates, votes]

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

def tallyCandidateVotes(candidateName, votes):

    tally = 0
    for vote in votes:
        if len(vote) > 1:
            if candidateName == vote[1]:
                tally += float(vote[0])

    return round(tally,5)

def processVotingData(candidates, votes, electionThreshold, seat_count):

    # Loop through the rounds
    amountToDistribute = 0
    winnerNumber = 0
    lastWinner = 0
    voteRound = 1

    for voteRound in range(len(candidates)):
        
        #If it is the last round, the last person wins.
        if voteRound == len(candidates)-1 and winnerNumber != seat_count:
            for candidate in candidates:
                if candidate['status'] == '':
                    candidate['status'] = 'Winner. Last Rnd'
            break

        # Tally votes
        for candidate in candidates:
            if candidate['status'] == '':
                candidate['prevTally'] = candidate['tally']
                candidate['tally'] = tallyCandidateVotes(candidate['name'], votes)

        pprint.pprint(candidates)
        
        # Determine if there is a winner.
        tallies = [candidate['tally'] for candidate in candidates]
        maxVotes = [i for i, x in enumerate(tallies) if x == max(tallies)]

        if candidates[maxVotes[0]]['tally'] > electionThreshold:
            # There is a winner
            lastWinner = maxVotes[0]
            winnerNumber += 1

            # Note the votes to distribute.
            totalVotesToDistribute = candidates[lastWinner]['tally'] - electionThreshold
            amountToDistribute = totalVotesToDistribute / candidates[lastWinner]['tally']
            candidates[lastWinner]['prevTally'] = candidates[lastWinner]['tally']
            candidates[lastWinner]['tally'] = -999
            candidates[lastWinner]['status'] = 'Winner. Rnd: ' + str(voteRound)

            # Loop through the votes
            for i in range(len(votes)):

                # Adjust weights
                if len(votes[i]) > 1:
                    if votes[i][1] == candidates[lastWinner]['name']:
                        votes[i][0] = str(round(float(votes[i][0]) * amountToDistribute,5))

                # Remove the person from the votes
                try:
                    votes[i].remove(candidates[lastWinner]['name'])
                except:
                    pass

        else:
            # There isn't a winner
            # Determine lowest tally.
            tallies = [abs(candidate['tally']) for candidate in candidates]
            minVotes = [i for i, x in enumerate(tallies) if x == min(tallies)]
            lastLoser = minVotes[-1]

            # Remove the candidates and note the amount to distribute.
            candidates[lastLoser]['status'] = 'Removed. Rnd ' + str(voteRound)
            candidates[lastLoser]['prevTally'] = candidates[lastLoser]['tally']
            candidates[lastLoser]['tally'] = -999

            # Remove the person
            for i in range(len(votes)):
                try:
                    votes[i].remove(candidates[lastLoser]['name'])
                except:
                    pass
        
        print('----------------')
        print("Round: " + str(voteRound))
        pprint.pprint(votes)

        voteRound += 1
        
            
    return candidates

def main():
    
    # Get the data
    seat_count = int(input("Number of seats:"))
    #print('===============================================================================================================================')
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
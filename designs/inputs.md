# Input Layer

## Owner
* Has a secret input they want to store (`I`)
* Split input into `n` shares where each share is (I~1~, I~2~, ..., I~n~)
* Invokes the smart contract's `storeData` function with the shares and their commitments
* Each person in a randomly selected quorum now holds a share of the input

### Quorum Selection (On-Chain)
* Gather the list of all active stakeholders
* Select a random `n` stakeholders to be the shareholders for this input
* Each share is encrypted and sent to the respective shareholder
* __Doesn't the owner have to send a key to each shareholder?__

### Share Renewel
_One quorum should never hold their shares for an extended period of time and thus we initiate a re-sharing protocol to transfer the shares to a new random quorum_
* Owner invokes the `renewShares` function on the smart contract which starts the selection of a new random quorum
* The current quorum then collectively generate (in batches) a new polynomial for each of their shares to mask the previous value
    * i.e. {V + W~k~} for each k in the new quorum
    * V should be unique for each k
* This polynomial needs to satisfy the following:
    * ∀𝑘 𝑈′𝑘(𝑖) = 𝑈(𝑖) + 𝑉(𝑖) + 𝑊𝑘(𝑖)
    * Where V(0) = 0 and ∀𝑘 𝑊𝑘(k) = k holds
* Each current member then stores its share for k as {U'~k~(i) = U(i) + V(i) + W~k~(i)} for each k
    * U(i) being the current shareholder's share
* Each new member in Q' collects t+1 shares and reconstructs the polynomial to get U'(k)

#### Obtaining V without interaction
* Each current shareholder can construct a Pseudo-Random Zero Sharing (PRZS) which supplies a polynomial such that V(0) = 0

n = 5
t = 3
s = 55
|A| = 2

1, 2, 3, 4, 5

A1 = (1, 2) = 1
A2 = (1, 3) = 2
A3 = (1, 4) = 3
A4 = (1, 5) = 4
A5 = (2, 3) = 5
A6 = (2, 4) = 6
A7 = (2, 5) = 7
A8 = (3, 4) = 8
A9 = (3, 5) = 9
A10 = (4, 5) = 10

1 = rA1 @ 1, rA2 @ 2, rA3 @ 3, rA4 @ 4
2 = rA1 @ 1, rA5 @ 5, rA6 @ 6, rA7 @ 7
3 = rA2 @ 2, rA5 @ 5, rA8 @ 8, rA9 @ 9
4 = rA3 @ 3, rA6 @ 6, rA8 @ 8, rA10 @ 10
5 = rA4 @ 4, rA7 @ 7, rA9 @ 9, rA10 @ 10

(x-3)(x-4)(x-5)+1
# COLLABORATOR RESPONSIBILITIES

## My schemas
- i have already written the schemas for dna
- will now design the api endpoints and routers


## Initial steps for shubh
 - make a dir name it wtv, preferably same as github repo
 - initialise and setup git in it, and connect to the github repo
 - then make a new branch using cmd : `git branch -b <branch-name> endpoints` or use GUI of github
 - now do wtv needed changes in this branch


## Following functions will be written by Shubh
 - dna validity check function -> takes DNASequence, returns a DNAValidityResponse.
 - dna analysis function -> takes DNASequence and DNAAnalysisOptions, returns a DNAAnalysisResponse. It shows:
  1. seq length
  2. gc content
  3. nucleotide count
  4. if it is a valid seq -> uses the validity function already defined
  5. reverse compliment of the seq

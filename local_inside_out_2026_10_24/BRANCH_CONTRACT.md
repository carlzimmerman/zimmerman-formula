# LIO-5: alternative basin and resolution check

LIO-4 failed the prepared front at n128. This final bounded test starts from
all T and minimizes the same response-weighted energy with the same free
exterior, seeking a different local minimum rather than rerunning the front.
Profiles1/2, environment2, ell30, n64/128/256. A high inner fraction alone
is insufficient: the outer mass must be free (q_outer<=.05), interior q>=.95,
stationarity and positive Hessian must be established. No optimizer success
flag substitutes for these checks. No exhaustive exclusion follows from
failure. The law diagnostic remains conditional and density is held fixed.

# What no jumps and no Cantor part would still fail to prove

Even proving SBV regularity and combining it with PF14's zero jump part would
only give a W1,1-type derivative statement. It would not restore the bounded
first derivatives needed by the strong continuation theorem.

The following is a countertest of that abstract inference, not an AC2q solution.
On a bounded spacetime region set y=x-c t and

    u(t,x)=c+delta sqrt(abs(y)),    delta>0.

Then u is continuous and locally W1,1 in spacetime, with no jump or Cantor
part, but its derivatives are not bounded near y=0. It satisfies the genuinely
nonlinear scalar balance law

    u_t+partial_x(u²/2)=(delta²/2) sign(x-c t)

almost everywhere and distributionally. Its source is bounded, but not
Lipschitz in x. Choose the region and delta small enough that u stays close
to any chosen nonzero subluminal c; compact values do not remove the cusp.

The characteristic equation x'=u(t,x) becomes

    y'=delta sqrt(abs(y)).

Starting from y=0, it admits waiting trajectories

    y(t)=0 for t<=t_wait,
    y(t)=delta²(t-t_wait)²/4 for t>=t_wait,

as well as y=0 throughout. Hence continuous W1,1 coefficients and a bounded
source alone do not give a unique classical characteristic flow. This is not
an example of nonunique PDE solutions, nor of continuation from the AC2q smooth
incoming data; the displayed field is fixed and its initial trace already has
a cusp. It only falsifies a proposed regularity/flow implication.

For AC2q, additional structure in the auxiliary constraints might exclude this
kind of behavior. That structure must be proved to supply the missing temporal
or source regularity. It cannot be inferred merely from genuine nonlinearity,
bounded source, zero jump part, or zero Cantor part. Likewise a characteristic
Riccati argument after breakdown cannot be used without first justifying its
flow and products in the chosen weak class.

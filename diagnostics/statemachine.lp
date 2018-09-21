%times
%time(1..15).

%temp states
temp(65..105).
temp(off).

%heating states
hstat(baking).
hstat(preheating).
hstat(heated).
hstat(finished).
hstat(idle).
hstat(off).

%loading states
lstat(notready).
lstat(ready).
lstat(loading).
lstat(loaded).
lstat(unloading).
lstat(unloaded).
lstat(off).

%define inertial fluents
%ls = loading status
%hs = heating status
%t = temperature
fluent(inertial, hs(X)) :- hstat(X).
fluent(inertial, ls(X)) :- lstat(X).
fluent(inertial, t(X)) :- temp(X).

%define actions
action(turnon).
action(place).
action(heat(X)) :- temp(X).
action(timepassed).
action(load).
action(unload).
action(remove).
action(turnoff).


%inertia axioms
hd(F, I2) :- hd(F, I), fluent(inertial, F), not -hd(F, I2), step(I), +(I,1,I2), not ab(F, I).
-hd(F, I2) :- -hd(F, I), fluent(inertial, F), not hd(F, I2), step(I), +(I,1,I2), not ab(F, I).

%CWA
-hd(F, I) :- not hd(F, I), step(I), fluent(defined, F).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%begin description of state transitions%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%
%describe turning on%
%%%%%%%%%%%%%%%%%%%%%
hd(hs(idle), I2) :- occ(turnon, I), hd(hs(off), I), step(I), +(I, 1, I2).
ab(hs(off), I):- occ(turnon, I), hd(hs(off), I), step(I).

hd(ls(notready), I2) :- occ(turnon, I), hd(ls(off), I), step(I), +(I, 1, I2).
ab(ls(off), I):- occ(turnon, I), hd(ls(off), I), step(I).

hd(t(70), I2) :- occ(turnon, I), hd(t(off), I), step(I), +(I, 1, I2).
ab(t(off), I):- occ(turnon, I), hd(t(off), I), step(I).

%%%%%%%%%%%%%%%%%%%%%%%
%place pod on the tool%
%%%%%%%%%%%%%%%%%%%%%%%
hd(ls(ready), I2) :- occ(place, I), hd(ls(notready), I), step(I), +(I, 1, I2).
ab(ls(notready), I) :- occ(place, I), hd(ls(notready), I), step(I).


%%%%%%%%%%%%%%%%%%%%%%%%%%
%describe heating process%
%%%%%%%%%%%%%%%%%%%%%%%%%%
hd(hs(preheating), I2) :- occ(heat(X), I), hd(hs(idle), I), step(I), +(I, 1, I2).
ab(hs(idle), I) :- occ(heat(X), I), hd(hs(idle), I), step(I).

%timepassed will be added by the listener or the simulator
hd(hs(heated), I2) :- occ(timepassed, I), occ(heat(X), I3), hd(hs(preheating), I), step(I), +(I, 1, I2), -(I, 1, I3).
ab(hs(preheating), I) :- occ(timepassed, I), occ(heat(X), I2), hd(hs(preheating), I), step(I), -(I, 1, I2).
hd(t(X), I2) :- occ(timepassed, I), occ(heat(X), I3), hd(hs(preheating), I), step(I), +(I, 1, I2), -(I, 1, I3).
ab(t(Y), I) :- occ(timepassed, I), occ(heat(X), I2), hd(t(Y), I), step(I), -(I, 1, I2).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%describe loading and baking process%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
hd(ls(loading), I2) :- occ(load, I), hd(hs(heated), I), step(I), +(I, 1, I2).
ab(ls(ready), I) :- occ(load, I), hd(hs(heated), I), step(I).

%baking
hd(hs(baking), I2) :- occ(timepassed, I), occ(load, I3), hd(ls(loading), I), step(I), +(I, 1, I2), -(I, 1, I3).
ab(hs(heated), I) :- occ(timepassed, I), occ(load, I2), hd(ls(loading), I), step(I), -(I, 1, I2).
hd(ls(loaded), I2) :- occ(timepassed, I), occ(load, I3), hd(ls(loading), I), step(I), +(I, 1, I2), -(I, 1, I3).
ab(ls(loading), I) :- occ(timepassed, I), occ(load, I2), hd(ls(loading), I), step(I), -(I, 1, I2).

%finished baking
hd(hs(finished), I2) :- occ(timepassed, I), hd(hs(baking), I), step(I), +(I, 1, I2).
ab(hs(baking), I) :- occ(timepassed, I), hd(hs(baking), I), step(I).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%describe unloading process%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%
hd(ls(unloading), I2) :- occ(unload, I), hd(hs(finished), I), hd(ls(loaded), I), step(I), +(I, 1, I2).
ab(ls(loaded), I) :- occ(unload, I), hd(hs(finished), I), hd(ls(loaded), I), step(I).

%unloading time has passed
hd(ls(unloaded), I2) :- occ(timepassed, I), hd(hs(finished), I), hd(ls(unloading), I), step(I), +(I, 1, I2).
ab(ls(unloading), I) :- occ(timepassed, I), hd(hs(finished), I), hd(ls(unloading), I), step(I).

%%%%%%%%%%%%
%remove pod%
%%%%%%%%%%%%
hd(ls(notready), I2) :- occ(remove, I), hd(ls(unloaded), I), step(I), +(I, 1, I2).
ab(ls(unloaded), I) :- occ(remove, I), hd(ls(unloaded), I), step(I).
hd(hs(idle), I2) :- occ(remove, I), hd(ls(unloaded), I), hd(hs(finished), I), step(I), +(I, 1, I2).
ab(hs(finished), I) :- occ(remove, I), hd(ls(unloaded), I), hd(hs(finished), I), step(I).

%%%%%%%%%%%%%%%%%%%%%
%describe turning off%
%%%%%%%%%%%%%%%%%%%%%
hd(hs(off), I2) :- occ(turnoff, I), hd(hs(idle), I), step(I), +(I, 1, I2).
ab(hs(idle), I):- occ(turnoff, I), hd(hs(idle), I), step(I).

hd(ls(off), I2) :- occ(turnoff, I), hd(ls(notready), I), step(I), +(I, 1, I2).
ab(ls(notready), I):- occ(turnoff, I), hd(ls(notready), I), step(I).

hd(t(off), I2) :- occ(turnoff, I), hd(t(X), I), step(I), temp(X), +(I, 1, I2).
ab(t(X), I):- occ(turnoff, I), hd(t(X), I), step(I), temp(X).

%%%%%%%%%%%%%%%%%%%
%diagnostic module%
%%%%%%%%%%%%%%%%%%%
-hd(F, I) :- not hd(F, I), fluent(inertial, F), step(I).
obs(F, false, I) :- not obs(F, true, I), inclstep(I), fluent(inertial, F).
occ(A, I) :- hpd(A, I), action(A), step(I).
:- obs(F, true, I), -hd(F, I), inclstep(I).
:- obs(F, false, I), hd(F, I), inclstep(I).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Will move to separate file%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%steps
step(1..1).
inclstep(1..2).

%initial states
hd(hs(off), 1).
hd(ls(off), 1).
hd(t(off), 1).
obs(hs(off), true, 1).
obs(ls(off), true, 1).
obs(t(off), true, 1).


%actions that occurred
hpd(turnon, 1).

obs(hs(idle), true, 2).
obs(ls(notready), true, 2).
obs(t(70), true, 2).
%hpd(place, 2).

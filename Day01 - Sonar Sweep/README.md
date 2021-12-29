# Day 1 - Sonar Sweep

This is the first and only day in which I utilize PowerShell. I was hoping to learn PowerShell a little more, but honestly my skills are at a point where these kinds of problems aren't enhancing my PS-fu. I need practice utilizing all the modules, which these kinds of problems (usually) won't accomplish. So from now on I'll be completing the days in Python (until Day 15 when I switch to C++).

Today was obviously a pretty trivial day, being the first day, however my co-worker Graham pointed out that my solution isn't optimal. I was summing the two sets, when really I only needed to compare the two outliers, since anything in between were shared by the two sets. For example, given the depths {A, B, C, D}, the first set is {A, B, C} and the second set is {B, C, D}. Since both sets contain {B, C}, I don't need to add those to the comparison and can just compare {A} and {D} directly.

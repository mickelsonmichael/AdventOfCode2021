# Day 17 - Trick Shot

Today is the first day where I'll be updating this journal (to the best of my abilities) as I work, attempting to record my train of thought. I won't record everything but I will record issues I encounter and hopefully writing them down will cement their solutions in my mind.

After the fact, it's very obvious that this is essentially a brain dump. If you're looking for an explanation on how to solve this one, I wouldn't necessarily read this for information. This was me spilling out my thoughts as they appeared, and they weren't always right or sensical (although I tried to fix that in post). Read at your own risk.

## Part 1

Here are some summary bullets as I read the prompt:

- Probe velocity should be an x,y coordinate with negative values (signed int)
  - Is there a way to do tuples in C++? There's the `std::pair` which could be good enough, or I could create a `struct` to allow more methods. Will need to read on.
- Probe position starts at `0,0` and move in steps based on velocity
- Velocity `x` decreases each step by `1` until it is `0` (+- 1 if negative or positive, it moves towards zero either way)
- Velocity `y` decreases by `1`, assumedly it can go negative until it is falling down the trench at terminal velocity
- Probe must hit a target area
  - Slightly unclear on this one, does it just need to eventually hit the target area? Will continue reading.
  - Further on it explains that the probe must "land" within the target area at the end of some step. If the steps span the target area but are not inside it, it is not considered a "hit"
- Grid should be increasing in `x` direction and decreasing in the `y`
- Part 1 Question: What is the highest `y` position that can be reached while still hitting the target area.

So it's clear I need to create several things. First off, a grid with increasing axes. I can use a standard multi-dimensional array for calculations, then flip the `y` axis when it needs to be printed so the display is correct. I'll likely start with just creating and displaying the grid and target area. Because the example is just a target area, I'll simply hard code it instead of creating my usual `Example.txt` to save on time.

After reading again, it would seem that the grid is not a pre-defined thing. The grid should only be large enough to fit the sub (`0,0`) and the target area, the trajectory of the probe can extend the grid if necessary. So perhaps it is best not to create a constraining, multi-dimensional array and just work directly with the coordinates and simply keep a list of "places" the probe has been.

I've now successfully created a mechanism for firing probes and displaying the results. The next step is to fire multiple probes (or figure it out mathematically) until I know the correct velocity at which to fire.

For the `x` direction, the probe will slow down until `0`, so I need to fire the probe so it either (a) eventually stops in a position within the target area or (b) passes through the target area while it slows down.
We can get a finite list of `x` velocities by checking everything between `1` and the maximum value of the target area; anything larger and we'll pass right over it on the first step. Something like `for (int i = min(min_target_x, 1); i <= max_target_x; ++i)` should be adequate, with each iteration checking if a probe fired straight at it would hit. It's important to keep in mind that some velocities may hit the target areas multiple times as well, but we only need on confirmed hit to add it to our list of potential `x` values. In the worst case scenario, where a target area covers an entire grid, our `x` values would be a list `INT32_MAX * 4` in size, which is a couple million, however this scenario is unlikely and our realistic worse-case would likely be somewhere in the magnitude of `1000` or fewer.

Once the candidates for `x` have been generated, we need to calculate a list of candidate `y` values. The `y` values should be tested individually against each `x` value in order to determine whether they hit. Since the `x` value are already determined, we should just consider they `y` component alone, and should get a list of `y` values that, when fired, will eventually hit inside the range of the target area. The minimal `y` value should be the one that lands on the minimum `y` of the target area. Next, we should check positive `y`, which will be a little more challenging. Technically, we could continue to increase our `y` value infinitely and there would be an infinite number of value, an infinite number of which would overflow our integer. This is where testing against the `x` component becomes crucial. Only testing `y` values until the first `y` value that, when fired, would result in the `x` component missing the target area.

I tried a few test loops and found that I was having troubles grokking the `y` component, so I started writing down trajectories (fired straight up) to find a pattern, and I have found one. The maximum number any `y` value can reach is `(n^2 + n) / 2`, or the sum of all its components between 0 and itself (e.g. for 5 that's `5+4+3+2+1`). This is apparently called the [nth triangle number](https://math.stackexchange.com/questions/593318/factorial-but-with-addition/593323). That will allow the height to be easily checked for values greather than `0`. Another pattern is that all `y` trajectories eventually hit exactly `y=0` as a step, then the following step will be `-y - 1` (e.g. for `5`, the first step after `y=0` will be `y=-6`). So therefore, if the minimum `y` value of the target area is below zero, the maximum positive `y` value we need to try is `y=-(min_target_y+1)` (e.g. for a target area with a minimum of `-10` like the example, the max `y` value we need to try is `9`; `9 -> 17 -> 24 -> 30 -> 35 -> 39 -> 42 -> 44 -> 45 -> 45 -> 44 -> 42 -> 39 -> 35 -> 30 -> 24 -> 17 -> 9 -> 0 -> -10`). 

Using this new information, I was able to restrict the `y` component into a smaller subset of values, meaning the number of values I have to test is significantly smaller. I can also save a few assignments by calculating the max height from the initial `y` value when I find a sucessful hit, instead of the `Probe` itself wasting time recording that information. With these lessons I've completed Part 1 and gotten the first star.

## Part 2

Part two seems trivial at first glance, perhaps I'm misunderstanding. But if not, then I've already got it solved. I have a function `get_y_values` and a function `get_x_values` that will return the possible values that will hit in those ranges. At it's most basic I could just multiply the length of those two lists together (e.g. 5 x 2 = 20 velocity values) but my gut tells me there are instances where an `x` and a `y` value don't mesh. I could be wrong, though, and instead of logic-ing it out, I'll just plug it in and see what I get.

My gut was correct but my code was not. After plugging in the example to my program, I realized I was missing several values, and that was simply due to the fact that I had forgotten I needed to do the ` max(target_max_y, 0)` to ensure if the target was below `0`, I started from `0` instead of from `target_max_y`. This netted me the correct answer for the example problem, but unfortunately my answer for the input was apparently too low. This leads me to a quandry, I'm unsure on how to proceed in debugging. I can try double-checking that I have all the values in the right place, which I will, but if that doesn't come up with the answer then I may be forced to print out all of the "missed" values and visually inspect which ones should have hit (or which ones had an error). I'm not looking forward to the process either way.

After analyzing my code extensively, I finally found the issue. While checking for `x` values within the range, I had the following simulation occuring:

```c++
  // simulate the firing
  int vel = x;
  int pos = x; // assume after the first step
  while (vel != 0 && pos < target.maxX)
  {
      pos += vel;
      vel -= x < 0 ? -1 : 1;

      if (pos >= target.minX && pos <= target.maxX)
      {
          x_values.push_back(x);
          break;
      }
  }
```

Critically, I was assuming that the first firing had already happend, since the first thing in the loop I did was check if the value was within the target range (which would be an automatic bullseye in the `x` range). But, I was incrementing the `pos` before decreasing the `vel` due to drag, which mean that a Probe fired at `5` using this simulation would go `5 -> 5 -> 4 -> 3 -> 2 -> 1` with a duplicate set of `5`. Swapping the two lines provided the correct answer to part 2, and it was only sheer luck that it allowed for the correct answer to part 1.

## Things Learned

### C++ Compiler Reorder Error

While creating the `TargetArea` class I experienced a unique C++ error `-Werror=reorder`. It is complaining that the intialization list of my class is not in the same order as the properties are defined. This is an issue because, even though you can put the initialization properties in order visually, C++ will initialize those properties in the order of their definition in the class. For example, in the following snippet, `b` is declared before `a` in the class, but the the constructor calls `a()` then `b()` (allegedly). In actuality `b()` will still called before `a()`, so this error is to help prevent issues where that order may matter (as dependencies).

```c++
struct Point
{
    // b declared before a
    int b;
    int a;

    Point(int x, int y)
        : a(x), b(y) // a() called before b()
        { }
}
```

### std::reverse

Most (if not all but I haven't checked) STL containers do not have a `.reverse` method built-in. So you can utilize the `std::reverse()` function within the `<algorithm>` import to perform the reverse **in-place**. This was helpful when printing out the grid since, for simplicity, I was working with the grid upside-down in code. As with many of the STL utility functions, the parameters are simply an iterator pointing to the beginning of the list (easily accessible using `vector.begin()`) and an iterator pointing to the end of the list (easily accessible using `vector.end()`). If you're tricky, you could also utilize this method to reverse subsections of a list, since you don't necessarily need to passs the `begin()` and `end()` iterators, but could instead pass any iterators pointing to any two points within the list.

```c++
std::vector<int> list = { 1, 2, 3, 4 };

std::reverse(list.begin(), list.end());

// list is now 4, 3, 2, 1
```

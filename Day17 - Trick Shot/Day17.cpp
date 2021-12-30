#include <iostream>
#include <assert.h>
#include <vector>
#include <set>
#include <algorithm>

using namespace std;

struct TargetArea
{
    const int minX;
    const int maxX;
    const int minY;
    const int maxY;
    const pair<int, int> start;

    TargetArea(const int &minX, const int &maxX, const int &minY, const int &maxY)
        : minX(minX), maxX(maxX), minY(minY), maxY(maxY), start(0, 0) {}

    bool is_above(const int &y) const
    {
        return y > maxY;
    }

    bool is_left(const int &x) const
    {
        return x < minX;
    }

    bool is_hit(const int &x, const int &y) const
    {
        return (x >= minX && x <= maxX) && (y >= minY && y <= maxY);
    }
};

struct Probe
{
    Probe(const int &initial_x_velocity, const int &initial_y_velocity)
        : x_pos(0), y_pos(0), x_velocity(initial_x_velocity), y_velocity(initial_y_velocity), is_fired(false), steps()
    {
    }

    // Fires the probe and returns true if it is a hit. A probe cannot be fired twice.
    bool fire(const TargetArea &t)
    {
        assert(!is_fired);
        is_fired = true;

        bool is_above_init = t.is_above(y_pos);
        bool is_left_init = t.is_left(x_pos);

        do
        {
            step();

            if (t.is_hit(x_pos, y_pos))
            {
                return true;
            }
        }
        // Only continue to step until we have missed the target area
        while (
            !(t.is_above(y_pos) != is_above_init && t.is_left(x_pos) != is_left_init) // when we pass through
            && !(t.minY > y_pos && y_velocity < 0)                                    // as long as the target isn't too high
            && !(t.minX > x_pos && x_velocity == 0)                                   // as long as we don't stop early on the right
            && !(t.maxX < x_pos && x_velocity == 0)                                   // as long as we don't stop early on the left
        );

        return false;
    }

    void printOn(const TargetArea &t, ostream &o = cout) const
    {
        assert(is_fired);

        // Initialize the area as the target area
        int maxX = t.maxX;
        int maxY = t.maxY;
        int minX = t.minX;
        int minY = t.minY;

        // Ensure the start area is inside the grid
        if (maxX < 0)
            maxX = 0;
        if (minX > 0)
            minX = 0;
        if (maxY < 0)
            maxY = 0;
        if (minY > 0)
            minY = 0;

        // Ensure every step is in side the grid
        for (pair<int, int> step : steps)
        {
            const int x = step.first;
            const int y = step.second;

            if (x > maxX)
                maxX = x;
            if (x < minX)
                minX = x;
            if (y > maxY)
                maxY = y;
            if (y < minY)
                minY = y;
        }

        // Ensure the minimum x and minimum y are within the bounds of a 0-based index
        int shiftX = 0;
        int shiftY = 0;

        if (minX < 0)
        {
            shiftX = -minX;
        }

        if (minY < 0)
        {
            shiftY = -minY;
        }

        vector<vector<char>> grid(maxY + shiftY + 1, vector<char>(maxX + shiftX + 1, '.'));
        grid[0 + shiftY][0 + shiftX] = 'S';

        // Print the target area
        for (int y = t.minY; y <= t.maxY; ++y)
            for (int x = t.minX; x <= t.maxX; ++x)
            {
                grid[y + shiftY][x + shiftX] = 'T';
            }

        // Print the steps
        for (pair<int, int> step : steps)
        {
            grid[step.second + shiftY][step.first + shiftX] = '#';
        }

        // Print to screen
        reverse(grid.begin(), grid.end());
        for (vector<char> row : grid)
        {
            for (char c : row)
            {
                o << c;
            }
            o << '\n';
        }
    }

private:
    int x_pos;
    int y_pos;
    int x_velocity;
    int y_velocity;
    bool is_fired;
    int max_height;
    vector<pair<int, int>> steps;

    void step()
    {
        x_pos += x_velocity;
        y_pos += y_velocity;
        --y_velocity;

        if (x_velocity != 0)
        {
            x_velocity -= x_velocity > 0 ? 1 : -1;
        }

        pair<int, int> step(x_pos, y_pos);
        steps.push_back(step);
    }
};

vector<int> get_x_values(const TargetArea &target)
{
    vector<int> x_values;

    for (int x = min(target.minX, 0); x <= target.maxX; ++x)
    {
        // if it's in the range of the area on the first shot, just add it
        if (x >= target.minX && x <= target.maxX)
        {
            x_values.push_back(x);
            continue;
        }

        // simulate the firing
        int vel = x;
        int pos = x; // assume after the first step
        while (vel != 0 && pos < target.maxX)
        {
            vel -= x < 0 ? -1 : 1;
            pos += vel;

            if (pos >= target.minX && pos <= target.maxX)
            {
                x_values.push_back(x);
                break;
            }
        }
    }

    // print to screen
    // cout << "x: ";
    // for (int x : x_values)
    //     cout << x << ", ";
    // cout << '\n';

    return x_values;
}

vector<int> get_y_values(const TargetArea &t)
{
    vector<int> y_values;
    int y;

    // Everything is above zero, we have to aim only up
    if (t.minY > 0)
    {
        // max number we need to try is the max y of the target area, everything else will miss on the first shot
        for (y = t.minY; y <= t.maxY; ++y)
            y_values.push_back(y);
    }
    // Some up, some down, or all down
    else if (t.maxY < 0)
    {
        // firing down
        for (y = 0; y >= t.minY; --y)
            y_values.push_back(y);

        // firing up
        for (y = 1; y <= 1 - t.minY; ++y)
            y_values.push_back(y);
    }

    // print to screen
    // cout << "y: ";
    // for (int y : y_values)
    //     cout << y << ", ";
    // cout << '\n';

    return y_values;
}

int find_max_height(const TargetArea &t)
{
    int max_height = INT32_MIN;
    vector<int> x_values = get_x_values(t);
    vector<int> y_values = get_y_values(t);

    for (int x : x_values)
    {
        for (int y : y_values)
        {
            Probe p(x, y);

            if (p.fire(t)) // if we hit
            {
                int probe_max_height = y > 0 ? ((y * y) + y) / 2 : y;

                if (probe_max_height > max_height)
                {
                    max_height = probe_max_height;
                }
            }
        }
    }

    return max_height;
}

size_t find_unique_velocities(const TargetArea &t)
{
    set<pair<int, int>> vals;
    vector<int> x_values = get_x_values(t);
    vector<int> y_values = get_y_values(t);

    for (int x : x_values)
    {
        for (int y : y_values)
        {
            Probe p(x, y);

            // if (x == 10)
            //     cout << "testing " << x << ", " << y << '\n';

            if (p.fire(t)) // if we hit
            {
                pair<int, int> pair(x, y);
                vals.insert(pair);
            }
        }
    }

    return vals.size();
}

int main()
{
    // Example x=20..30, y=-10..-5
    // TargetArea target(20, 30, -10, -5);

    // Input x=269..292, y=-68..-44
    TargetArea target(269, 292, -68, -44);

    // Probe p(269, -68);
    // p.fire(target);
    // p.printOn(target);

    // int max_height = find_max_height(target);
    // cout << "Max height: " << max_height << '\n';

    size_t num_vel = find_unique_velocities(target);
    cout << "Number of values: " << num_vel << '\n';

    return EXIT_SUCCESS;
}

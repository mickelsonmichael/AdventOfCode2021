# Day 16 - Chiton

This is the first day I'm switching over to utilizing C++. Up until this point I've been using Python which is incredibly pleasant to write with, I have to admit, especially for these brief scenarios. However, because it's so simple I eventually hit a wall where I didn't feel like I was learning much else; my return on investment was quickly diminishing. Thus, since I should know C++ better for my work, I decided to switch over.

Setting up my environment was by **far** the biggest time sink. I attempted to use the [Visual Studio development containers](https://code.visualstudio.com/docs/remote/containers) feature, but initially had troubles getting the container to start. Fast forward a little while and I've figured out that it's an issue with my company's corporate proxy; the container can't utilize `curl` or `pip` because neither can verify the certificate chain. Luckily, the development containers provide a base `Dockerfile` which I could use to my advantage, and all I needed to do was to disable secure connections using config files. **This is not the safest method**, I'll admit. It leaves me very vulnerable, and the proper was to do this would have been to place the required certificate into the container and add it to the store, but this was much faster. Likely later down the road I should do my best to add the certificate in.

As for the problem itself, I realized very quickly that it was a simple case of traversing a graph. Having just taken the appropriate course at Colorado State University (Online, I'm going for a second major with my first being in Biological Sciences), I knew how to readily traverse a tree. However, I didn't acknowledge the fact that it was a weighted tree for some time, and I wasted precious time tring to implement a breadth-first search. Eventually I realized that Dijkstra's algorithm was the way to go and that helped things go along much smoother.

The second largest time sink was also partially due to my environment. I wasn't able to install the C++ extension(s) for VS Code, again because of the corporate proxy, so I was flying by the seat of my pants and using the compiler to check for syntax errors. This also meant that I didn't have predictions enabled, so I had no idea what methods each class had. This lead to a lot of exploring of the C++ documentation to determine what types of STL containers to use and when. This was good because I learned more about the STL containers, but bad because I spent a ton of excessive time to do it.

While attempting to grok the Dijkstra's algorithm (and why my code was taking so long, turns out my queue size was too large), I found a helpful person on reddit who was recording their solutions along with some supporting text in a markdown file. I really liked that approach so this is technically the first day I'm writing the README.md files associated with each day (technically I started them on Day 16 but I got the idea on this day). I'll make a good effort to go back and write notes for the previous days.

Things I've improved on today:

- Refresh on how to structure a .cpp file
- Refresh on STL containers
- Practice at implementing Dijkstra's algorithm

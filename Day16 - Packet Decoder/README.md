# Day 16 - Packet Decoder

Today was extremely tedious. The actual solution itself wasn't very difficult, it was the build-up to it that was the pain. It required reading paragraph after paragraph of information on how to parse a binary string. No doubt this skill is useful, especially considering I know some applications I'm responsible for do a bit of binary messaging, but figure out the message format took a while to grok.

In the end I ended up using a simple `class` called `Packet`. The root `Packet` will parse the initial hex string, but then all child packets would simply receive a binary string and an index into that binary string. Using the index, they would parse themselves, then the parent could record the newly updated index and update its own before moving on to the next child `Packet`.

Thankfully, once part 1 was completed, part 2 was extremely trivial and only required several `if..else` statements. Beyond that nothing fancy.

Things I've improved on using this day:

- Converting an integer to a binary string, hex string, etc.
- The proper layout of a class
- Fixed the C++ extension so it is actually installed on the container and I get intellisense

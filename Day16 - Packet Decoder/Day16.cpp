// https://adventofcode.com/2021/day/16
// clear && g++ -Wall -Wextra -Werror -std=c++20 ./Day16.cpp && ./a.out
// or run ./run.sh

#include <iostream>
#include <sstream>
#include <bitset>
#include <string>
#include <assert.h>
#include <vector>
#include <fstream>

using namespace std;

// Converts a string to an integer with a base of 2 by default (16 for Hex)
unsigned long str_to_val(const string &str, const int &base = 2)
{
    return stoul(
        str,
        nullptr, // size_t* to store the number of characters processed
        base);
}

class Packet
{
    size_t current_bit;
    vector<Packet> packets;
    unsigned long value;
    string bit_string;

    // Retrieve the next slice of information and increase the current bit
    string next(const size_t &n = 0)
    {
        if (this->current_bit + n > this->bit_string.size()) {
            throw invalid_argument("gone too far!");
        }

        string result = this->bit_string.substr(this->current_bit, n);
        this->current_bit += n;
        return result;
    }

    // The first three bits encode the packet version
    void parse_version()
    {
        cout << "-> parsing version";
        string version_str = next(3);

        this->version = str_to_val(version_str);

        cout << " = " << this->version << '\n';
    }

    // The [second] three bits encode the packet type ID
    void parse_type_id()
    {
        cout << "-> parsing type id ";

        string type_id_str = next(3);

        this->type_id = str_to_val(type_id_str);

        cout << " = " << this->type_id << '\n';
    }

    void parse_literal()
    {
        cout << "-> parsing literal";

        vector<string> values;

        while (this->current_bit < this->bit_string.size())
        {
            string segment = next(5);

            values.push_back(segment.substr(1));
            cout << "\t" << segment;

            // The final segment has a trailing zero
            if (segment.find('0') == 0)
            {
                break;
            }
        }

        string binary_string;
        for (string str : values)
        {
            binary_string += str;
        }
        this->value = str_to_val(binary_string);

        cout << " = " << this->value << '\n';
    }

    void parse_operator()
    {
        cout << "-> parsing operator";

        // Every other type of packet (id != 4) represent an operator
        // An operator packet contains one or more packets
        string length_type_id = next(1);

        cout << " with length type id " << length_type_id << '\n';

        if (length_type_id == "0")
        {
            // If 0, the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet
            const unsigned long sub_packet_length = str_to_val(next(15));
            const unsigned long end = this->current_bit + sub_packet_length;

            while (this->current_bit < end)
            {
                Packet next(this->bit_string, this->current_bit);

                this->packets.push_back(next);
                this->current_bit = next.current_bit;
            }
        }
        else
        {
            // If 1, the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet
            const unsigned long sub_packet_count = str_to_val(next(11));

            for (size_t i = 0; i < sub_packet_count; ++i)
            {
                cout << "sub-packet " << i << '\n';
                Packet next(this->bit_string, this->current_bit);

                this->packets.push_back(next);
                this->current_bit = next.current_bit;
            }
        }

        // Packets with type ID 0 are sum packets
        if (this->type_id == 0)
        {
            this->value = 0;

            for (Packet p : this->packets)
            {
                this->value += p.value;
            }
        }
        // Packets with ID 1 are product packets
        else if (this->type_id == 1)
        {
            this->value = 1;

            for (Packet p : this->packets)
            {
                this-> value *= p.value;
            }
        }
        // Packets with ID 2 are minimum packets
        else if (this->type_id == 2)
        {
            this->value = this->packets[0].value;

            for (Packet p : this->packets)
            {
                if (p.value < this->value)
                {
                    this->value = p.value;
                }
            }
        }
        // Packets with ID 3 are maximum packets
        else if (this->type_id == 3)
        {
            this->value = 0;

            for (Packet p : this->packets)
            {
                if (p.value > this->value)
                {
                    this->value = p.value;
                }
            }
        }
        // Packets with ID 5 are greater than packets
        else if (this->type_id == 5)
        {
            assert(this->packets.size() == 2); // size must always be two

            this->value = this->packets[0].value > this->packets[1].value ? 1 : 0;
        }
        // Packets with ID 6 are less than packets
        else if (this->type_id == 6)
        {
            assert(this->packets.size() == 2); // size must always be two

            this->value = this->packets[0].value < this->packets[1].value ? 1 : 0;
        }
        // Packets with ID 7 are euqal to packets
        else if (this->type_id == 7)
        {
            assert(this->packets.size() == 2); // size must always be two

            this->value = this->packets[0].value == this->packets[1].value ? 1 : 0;
        }
        else
        {
            throw invalid_argument("unable to parse packet type id " + to_string(this->type_id));
        }
    }

    void parse()
    {
        parse_version();
        parse_type_id();

        // Packets with type ID 4 represent a literal value
        // Literal value packets encode a single binary number
        if (this->type_id == 4)
        {
            parse_literal();
        }
        else
        {
            parse_operator();
        }
    }

public:
    unsigned short version;
    unsigned short type_id;
    unsigned short length_type_id;

    Packet(const string &binary_string, const size_t &start_bit)
        : current_bit(start_bit), bit_string(binary_string)
    {
        cout << "starting sub-packet at bit " << start_bit << '\n';

        parse();
    }

    Packet(const string &hex_string)
        : current_bit(0), version(0), type_id(0)
    {
        cout << "starting base packet\n";

        stringstream ss;
        for (const char c : hex_string)
        {
            string str(1, c);

            unsigned long n = str_to_val(str, 16);
            bitset<4> b(n);

            ss << b;
        }
        this->bit_string = ss.str();

        parse();
    }

    unsigned get_version_sum() const
    {
        unsigned sum = this->version;

        for (Packet p : this->packets)
        {
            sum += p.get_version_sum();
        }

        return sum;
    }

    void dump() const
    {
        cout << "bits: " << this->bit_string << '\n'
             << "version: " << this->version << '\n'
             << "type id: " << this->type_id << '\n'
             << "value: " << this->value << '\n'
             << "sub-packets: " << this->packets.size() << '\n'
             << "version sum: " << get_version_sum() << '\n';
    }
};

int main()
{
    string example = "9C0141080250320F1802104A08";

    stringstream ss;
    ifstream file("Input.txt");
    ss << file.rdbuf();
    file.close();
    string input = ss.str();

    Packet outer_packet(input);

    outer_packet.dump();
}

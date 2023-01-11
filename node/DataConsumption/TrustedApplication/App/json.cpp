#include <iostream>
#include <fstream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main()
{
    // Open the JSON file
    std::ifstream json_file("example.json");

    // Parse the JSON data
    json data = json::parse(json_file);

    // Print the parsed JSON data to the console
    std::cout << data << std::endl;

    return 0;
}

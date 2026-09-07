#include <iostream>
#include <event2/event.h>
int main()
{    
    std::cout << "event version" << event_get_version()  << std::endl;
    return 0;
}
#include <iostream>
#include <chrono>
#include "eventList.h"
#include "epoch.h"
#include "sequence.h"


using namespace std;
using namespace std::chrono;

int main()
{
  cout << "Hello world!" << endl;

  string fn = "events.txt";
  eventList l(fn);

  system_clock::time_point t2, t1 = system_clock::now();
  while (1)
  {
    t2 = t1;
    for (int i = 0; i < 50; i++ ) cout << endl;
    l.printListCountdown();
    do t1 = system_clock::now(); while ((t1-t2)<seconds(1));
  }

  cout << endl << "hit enter ";
  cin.ignore();
  return 0;
}

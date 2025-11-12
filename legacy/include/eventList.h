#ifndef EVENTLIST_H
#define EVENTLIST_H

#include <set>
#include "event.h"

using namespace std;

//class event;

class compareEvents
{
  public:
    bool operator()(event* t1, event* t2);
};

class eventList
{
  private:
    typedef set<event*, compareEvents> eset;
    typedef eset::iterator eseti;
    eset m_collection;

    static string trim(string s);
    static string tokenize(string tokens, const string &s, size_t &a,
      size_t &z);

    int getLongestFqDesc() const;
    //int getLongestShortDesc() const;

  public:
    eventList(){};
    eventList(string filename);

    void addEvent(event* x);
    void removeEvent(event* x);
    void deleteEvent(event* x) {delete *(m_collection.find(x)); return;}

    void printList() const;
    void printListCountdown() const;

    void fromSerialized(string s);
};

#endif // EVENTLIST_H

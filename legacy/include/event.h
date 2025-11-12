#ifndef EVENT_H
#define EVENT_H

#include <chrono>
#include <string>
#include <vector>
//#include "eventList.h"

using namespace std;
using namespace std::chrono;

class sequence;
class eventList;

class event
{
  private:
    static const string weekdaystr[];
    static const char weekdayc[];

  protected:
    typedef time_point<system_clock, milliseconds> mstp;
    typedef duration<int,ratio<86400>> days;
    typedef vector<sequence*>::iterator vseqi;
    typedef vector<eventList*>::iterator vlisti;

    string m_desc;
    vector<sequence*> m_children;
    vector<eventList*> m_lists;

  public:
    enum weekday {sun,mon,tue,wed,thu,fri,sat};

    event(string desc = ""): m_desc(desc){};
    virtual ~event();

    bool operator<(const event& rhs) const
      {return this->getGmtEpoch() < rhs.getGmtEpoch();}
    bool operator>(const event& rhs) const {return rhs < *this;}
    bool operator<=(const event& rhs) const {return !(*this > rhs);}
    bool operator>=(const event& rhs) const {return !(*this < rhs);}
    bool operator==(const event& rhs) const
      {return this->getGmtEpoch() == rhs.getGmtEpoch();}
    bool operator!=(const event& rhs) const {return !(*this == rhs);}

    void setDesc(string desc) {m_desc = desc; return;}
    string getDesc() const {return m_desc;}
    string getFqDesc(bool omitanchor = false) const;
    //string getShortDesc() const;
    virtual mstp getGmtEpoch() const = 0;
    virtual mstp getSgmtEpoch() const = 0;

    string ymdhms() const;
    string deltanow() const;

    virtual event* getAnchor() const = 0;
    virtual void setAnchor(event* anchor) = 0;
    void addChild(sequence* x);
    void removeChild(sequence* x);
    void addList(eventList* x);
    void removeList(eventList* x);
};

#endif // EVENT_H

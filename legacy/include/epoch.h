#ifndef EPOCH_H
#define EPOCH_H

#include <string>
#include <chrono>
#include "event.h"

using namespace std::chrono;

class epoch: public event
{
  private:
    static milliseconds sgmtoffset;

    mstp m_epoch;

    mstp getGmtEpoch() const {return m_epoch - sgmtoffset;}
    mstp getSgmtEpoch() const {return m_epoch;}

  public:
    epoch():
      event("Now"),
      m_epoch(time_point_cast<milliseconds>(system_clock::now())){}
    epoch(string desc, short y, char mo, char d, char h, char m, float s,
      short tz_min_offset = 0):
      event(desc)
      {setEpoch(y,mo,d,h,m,s,tz_min_offset); return;}
    epoch(string desc, short y, short doy, char h, char m, float s,
      short tz_min_offset = 0):
      event(desc)
      {setEpoch(y,doy,h,m,s,tz_min_offset); return;}
    epoch(const epoch& x);
    ~epoch();

    static bool isDst(short y, char m, char d, char h);
    static bool leapYear(short y) {return !(y%400)+!(y%4)-!(y%100);}
    static void setSGMT(epoch sgmt, epoch rtgmt)
      {sgmtoffset = sgmt.m_epoch-rtgmt.m_epoch; return;}

    void setEpoch(short y, short doy, char h, char m, float s,
      short tz_min_offset = 0)
      {m_epoch = doyhmstz2GmtTp(y,doy,h,m,s,tz_min_offset); return;}
    void setEpoch(short y, char mo, char d, char h, char m, float s,
      short tz_min_offset = 0)
      {m_epoch = ymdhmstz2GmtTp(y,mo,d,h,m,s,tz_min_offset); return;}

    event* getAnchor() const {return NULL;}
    void setAnchor(event* anchor);

  private:
    // date static methods
    static char endOfMonth(short y, char m);
    static weekday ymd2wday(short y, char m, char d);
    static char firstWeekdayOfMonth(short y, char m, weekday d)
      {return 1+(d-ymd2wday(y,m,1)+7)%7;}

    // mstp methods
    static mstp ymdhmstz2GmtTp(short y, char mo, char d, char h, char m,
      float s, short tz = 0);
    static mstp doyhmstz2GmtTp(short y, short doy, char h, char m, float s,
      short tz = 0);
};

#endif // EPOCH_H

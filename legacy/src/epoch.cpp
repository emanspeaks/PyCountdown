#include "epoch.h"
#include "sequence.h"
#include "eventList.h"
#include <iostream>

milliseconds epoch::sgmtoffset(0);

epoch::epoch(const epoch& rhs)
{
  *this = rhs;
  vector<sequence*> tmp = m_children;
  m_children.clear();
  //m_lists.clear();

  for (vseqi i = tmp.begin(); i != tmp.end(); i++)
    {
      cout << *i << endl;
      (new sequence(**i))->setAnchor(this);
    }

  for (vlisti i = m_lists.begin(); i != m_lists.end(); i++)(*i)->addEvent(this);

  return;
}

epoch::~epoch()
{
  //dtor
}

bool epoch::isDst(short y, char m, char d, char h)
{
  /* dst notes
   *
   * spring forward second sunday march
   * fall back first sunday nov
   * http://www.timeanddate.com/laws/us/energypolicyact2005.html
   *
   * pretending all times are GMT for a consistent reference
   */
  mstp x = ymdhmstz2GmtTp(y,m,d,h,0,0);
  mstp dstStart = ymdhmstz2GmtTp(y,3,firstWeekdayOfMonth(y,3,sun)+7,2,0,0);
  mstp dstEnd = ymdhmstz2GmtTp(y,11,firstWeekdayOfMonth(y,11,sun),1,0,0);

  //If h = 2 on DST start, advance it to 3am (CDT) and assume DST.
  //If h = 1 on DST end, advance to the "second" 1am and assume NO DST.
  return (x >= dstStart && x < dstEnd);
}

void epoch::setAnchor(event* anchor)
{
  while (m_children.begin() != m_children.end())
    (*(m_children.begin()))->setAnchor(anchor);
  return;
}

char epoch::endOfMonth(short y, char m)
{
  struct tm t;
  t.tm_year = y-1900; // year since 1900
  t.tm_mon = m;      // month of year (0 .. 11)
  t.tm_mday = 0;       // day of month (0 .. 31)
  t.tm_hour = 0;      // hour of day (0 .. 23)
  t.tm_min = 0;        // minute of hour (0 .. 59)
  t.tm_sec = 0;        // second of minute (0 .. 59 and 60 for leap seconds)
  t.tm_isdst = -1;       // determine whether daylight saving time

  mktime(&t);
  return t.tm_mday;
}

event::weekday epoch::ymd2wday(short y, char m, char d)
{
  struct tm t;
  t.tm_year = y-1900; // year since 1900
  t.tm_mon = m-1;      // month of year (0 .. 11)
  t.tm_mday = d;       // day of month (0 .. 31)
  t.tm_hour = 0;      // hour of day (0 .. 23)
  t.tm_min = 0;        // minute of hour (0 .. 59)
  t.tm_sec = 0;        // second of minute (0 .. 59 and 60 for leap seconds)
  t.tm_isdst = -1;       // determine whether daylight saving time

  mktime(&t);
  return (weekday)(t.tm_wday);
}

event::mstp epoch::ymdhmstz2GmtTp(short y, char mo, char d, char h, char m,
  float s, short tz)
{
  // create system time
  struct tm t;
  t.tm_year = y-1900; // year since 1900
  t.tm_mon = mo-1; // month of year (0 .. 11)
  t.tm_mday = d; // day of month (0 .. 31)
  t.tm_hour = h; // hour of day (0 .. 23)
  t.tm_min = m; // minute of hour (0 .. 59)
  t.tm_sec = 0; // second of minute (0 .. 59 and 60 for leap seconds)
  t.tm_isdst = 0; // determine whether daylight saving time

  // convert to "local" to eliminate system TZ/DST on date
  // "local" means date entered, but may not be GMT
  time_t sys = mktime(&t);
  t = *gmtime(&sys);
  time_t local = 2*sys - mktime(&t); //sys-(gmt-sys), where (gmt-sys) is sys TZ

  // create mstp and subtract TZ and add seconds
  return time_point_cast<milliseconds>(system_clock::from_time_t(local))
    - minutes(tz) + milliseconds((unsigned short)(s*1000));
}

event::mstp epoch::doyhmstz2GmtTp(short y, short doy, char h, char m, float s,
  short tz)
{
  if (doy > (365 + leapYear(y))) throw "doy too large";

  char d;
  char mo = 0;
  do d = doy; while ((doy -= endOfMonth(y,++mo)) > 0);
  return ymdhmstz2GmtTp(y,mo,d,h,m,s,tz);
}
